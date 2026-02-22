"""
Animation Generator Module

This module handles the complete pipeline for generating Manim animations from natural language prompts:
1. AnimationPlanner - Creates structured animation plan from user prompt
2. ManimCodeGenerator - Generates Python/Manim code from the plan
3. AnimationRenderer - Renders the animation video using Manim CLI
"""

import os
import re
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


PROMPTS_DIR = Path("prompts")
PROMPT_CONFIG_PATH = PROMPTS_DIR / "prompt_config.json"
DEFAULT_PROMPT_CONFIG = {
    "planner_prompt_file": "planner_system_prompt.txt",
    "code_gen_prompt_file": "code_gen_system_prompt.txt",
}


def _render_prompt_template(template: str, values: dict[str, str]) -> str:
    """Replace known placeholders without failing on unknown placeholders."""
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{key}}}", value)
    return rendered


def _load_prompt_config() -> dict:
    """Load prompt file selection from config, with defaults as fallback."""
    if not PROMPT_CONFIG_PATH.exists():
        return DEFAULT_PROMPT_CONFIG.copy()

    try:
        config = json.loads(PROMPT_CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {PROMPT_CONFIG_PATH}: {exc.msg}"
        ) from exc

    merged_config = DEFAULT_PROMPT_CONFIG.copy()
    merged_config.update({k: v for k, v in config.items() if isinstance(v, str)})
    return merged_config


def _get_prompt_template(config_key: str) -> str:
    """Read selected prompt template from prompts directory based on config key."""
    config = _load_prompt_config()
    selected_file = config.get(config_key)

    if not isinstance(selected_file, str) or not selected_file.strip():
        raise ValueError(f"Prompt config key '{config_key}' must be a non-empty string")

    prompt_path = (PROMPTS_DIR / selected_file).resolve()
    prompts_dir_resolved = PROMPTS_DIR.resolve()

    try:
        prompt_path.relative_to(prompts_dir_resolved)
    except ValueError as exc:
        raise ValueError(
            f"Prompt file for '{config_key}' must be inside '{PROMPTS_DIR}'"
        ) from exc

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Configured prompt file not found for '{config_key}': {prompt_path}"
        )

    return prompt_path.read_text(encoding="utf-8")


class AnimationPlanner:
    """Generates a structured animation plan from a natural language prompt using Gemini."""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in your .env file. "
                "Get your API key from: https://makersuite.google.com/app/apikey"
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
    
    def generate_plan(self, user_prompt: str) -> tuple[str, dict]:
        """
        Generate a structured animation plan from user prompt.
        
        Args:
            user_prompt: Natural language description of desired animation
            
        Returns:
            Tuple of (plan_text, token_usage_dict)
            where token_usage_dict contains 'input_tokens' and 'output_tokens'
        """
        planner_template = _get_prompt_template("planner_prompt_file")
        full_prompt = _render_prompt_template(
            planner_template,
            {"user_prompt": user_prompt}
        )

        if "{user_prompt}" not in planner_template:
            full_prompt = f"{full_prompt}\n\nUser Request: {user_prompt}"
        
        response = self.model.generate_content(full_prompt)
        
        # Extract token usage from response metadata
        token_usage = {
            'input_tokens': response.usage_metadata.prompt_token_count,
            'output_tokens': response.usage_metadata.candidates_token_count
        }
        
        return response.text, token_usage


class ManimCodeGenerator:
    """Generates Manim Python code from an animation plan using Gemini."""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in your .env file."
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
        self.output_file = Path("src/generated_animations.py")
    
    def generate_code(self, animation_plan: str, user_prompt: str) -> tuple[str, str, dict]:
        """
        Generate Manim code from animation plan.
        
        Args:
            animation_plan: Structured plan with animation steps
            user_prompt: Original user prompt (for context)
            
        Returns:
            Tuple of (generated_code, class_name, token_usage_dict)
            where token_usage_dict contains 'input_tokens' and 'output_tokens'
        """
        # Create unique class name based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        class_name = f"GeneratedScene_{timestamp}"
        
        template = _get_prompt_template("code_gen_prompt_file")

        system_prompt = _render_prompt_template(
            template,
            {
                "class_name": class_name,
                "animation_plan": animation_plan,
                "plan_output": animation_plan,
                "user_prompt": user_prompt,
            }
        )
        
        response = self.model.generate_content(system_prompt)
        generated_code = response.text
        
        # Extract token usage from response metadata
        token_usage = {
            'input_tokens': response.usage_metadata.prompt_token_count,
            'output_tokens': response.usage_metadata.candidates_token_count
        }
        
        # Clean up the code (remove markdown code blocks if present)
        generated_code = self._clean_code(generated_code)
        
        # Ensure the class name is correct
        generated_code = self._ensure_class_name(generated_code, class_name)
        
        # Write to file
        self.output_file.write_text(generated_code, encoding='utf-8')
        
        return generated_code, class_name, token_usage
    
    def _clean_code(self, code: str) -> str:
        """Remove markdown code blocks and extra whitespace."""
        # Remove markdown code blocks
        code = re.sub(r'```python\s*', '', code)
        code = re.sub(r'```\s*', '', code)
        
        # Remove leading/trailing whitespace
        code = code.strip()
        
        return code
    
    def _ensure_class_name(self, code: str, expected_class_name: str) -> str:
        """Ensure the class name matches expected name."""
        # Find class definition and replace with expected name
        pattern = r'class\s+\w+\(Scene\)'
        replacement = f'class {expected_class_name}(Scene)'
        code = re.sub(pattern, replacement, code)
        
        return code


class AnimationRenderer:
    """Renders Manim animations using subprocess calls to the Manim CLI."""
    
    def __init__(self):
        self.media_dir = Path("media/videos/generated_animations")
    
    def render(self, class_name: str) -> tuple[bool, str, str]:
        """
        Render a Manim animation.
        
        Args:
            class_name: Name of the Manim Scene class to render
            
        Returns:
            Tuple of (success: bool, video_path_or_error: str, output_log: str)
        """
        command = [
            "manim",
            "-ql",  # Low quality for speed
            "src/generated_animations.py",
            class_name
        ]
        
        try:
            # Run manim command
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            output_log = result.stdout + "\n" + result.stderr
            
            if result.returncode != 0:
                return False, f"Rendering failed: {result.stderr}", output_log
            
            # Find the generated video file
            video_path = self._find_latest_video(class_name)
            
            if video_path and video_path.exists():
                return True, str(video_path), output_log
            else:
                return False, "Video file not found after rendering", output_log
                
        except subprocess.TimeoutExpired:
            return False, "Rendering timed out (>2 minutes)", ""
        except FileNotFoundError:
            return False, "Manim not found. Please install manim: pip install manim", ""
        except Exception as e:
            return False, f"Rendering error: {str(e)}", ""
    
    def _find_latest_video(self, class_name: str) -> Path:
        """Find the most recently created video file for the given scene."""
        # Manim saves videos to media/videos/{script_name}/{quality}/{scene_name}.mp4
        possible_paths = [
            Path(f"media/videos/generated_animations/480p15/{class_name}.mp4"),
            Path(f"media/videos/generated_animations/720p30/{class_name}.mp4"),
            Path(f"media/videos/generated_animations/1080p60/{class_name}.mp4"),
        ]
        
        # Check each possible path
        for path in possible_paths:
            if path.exists():
                return path
        
        # If not found in expected locations, search the entire media directory
        if self.media_dir.exists():
            video_files = list(self.media_dir.rglob("*.mp4"))
            if video_files:
                # Return the most recently modified video
                return max(video_files, key=lambda p: p.stat().st_mtime)
        
        return None


def generate_animation(user_prompt: str, logger=None) -> dict:
    """
    Complete pipeline: prompt -> plan -> code -> render.
    
    Args:
        user_prompt: Natural language description of desired animation
        logger: Optional callback function for logging (defaults to print)
        
    Returns:
        Dictionary with keys: success, plan, code, video_path, error, logs, token_usage
    """
    if logger is None:
        logger = print
    
    logger(f"[INPUT] User prompt: {user_prompt}")
    
    result = {
        "success": False,
        "plan": "",
        "code": "",
        "class_name": "",
        "video_path": "",
        "error": "",
        "logs": "",
        "token_usage": {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "plan_input_tokens": 0,
            "plan_output_tokens": 0,
            "code_input_tokens": 0,
            "code_output_tokens": 0,
            "input_cost_usd": 0.0,
            "output_cost_usd": 0.0,
            "total_cost_usd": 0.0
        }
    }
    
    try:
        # Step 1: Generate plan
        logger("[PLAN] Creating animation plan...")
        planner = AnimationPlanner()
        plan, plan_tokens = planner.generate_plan(user_prompt)
        result["plan"] = plan
        result["token_usage"]["plan_input_tokens"] = plan_tokens['input_tokens']
        result["token_usage"]["plan_output_tokens"] = plan_tokens['output_tokens']
        logger(f"[PLAN] Plan completed ({plan_tokens['output_tokens']} tokens)")
        
        # Step 2: Generate code
        logger("[CODE] Generating Manim code...")
        code_gen = ManimCodeGenerator()
        code, class_name, code_tokens = code_gen.generate_code(plan, user_prompt)
        result["code"] = code
        result["class_name"] = class_name
        result["token_usage"]["code_input_tokens"] = code_tokens['input_tokens']
        result["token_usage"]["code_output_tokens"] = code_tokens['output_tokens']
        logger(f"[CODE] Code generated ({code_tokens['output_tokens']} tokens)")
        
        # Calculate totals and costs
        total_input = plan_tokens['input_tokens'] + code_tokens['input_tokens']
        total_output = plan_tokens['output_tokens'] + code_tokens['output_tokens']
        
        # Pricing: $0.5 per 1M input tokens, $3 per 1M output tokens
        input_cost = (total_input / 1_000_000) * 0.5
        output_cost = (total_output / 1_000_000) * 3.0
        
        result["token_usage"]["total_input_tokens"] = total_input
        result["token_usage"]["total_output_tokens"] = total_output
        result["token_usage"]["input_cost_usd"] = input_cost
        result["token_usage"]["output_cost_usd"] = output_cost
        result["token_usage"]["total_cost_usd"] = input_cost + output_cost
        
        # Step 3: Render animation
        logger("[RENDER] Rendering animation video...")
        renderer = AnimationRenderer()
        success, video_or_error, logs = renderer.render(class_name)
        result["logs"] = logs
        logger("[RENDER] Rendering completed")
        
        if success:
            result["success"] = True
            result["video_path"] = video_or_error
            logger(f"[SUCCESS] Animation generated successfully: {video_or_error}")
        else:
            result["error"] = video_or_error
            logger(f"[ERROR] Rendering failed: {video_or_error}")
            
    except Exception as e:
        error_msg = f"Error in animation generation pipeline: {str(e)}"
        result["error"] = error_msg
        logger(f"[ERROR] {error_msg}")
    
    return result
