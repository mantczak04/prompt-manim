"""
Animation Generator Module

This module handles the complete pipeline for generating Manim animations from natural language prompts:
1. AnimationPlanner - Creates structured animation plan from user prompt
2. ManimCodeGenerator - Generates Python/Manim code from the plan
3. AnimationRenderer - Renders the animation video using Manim CLI
"""

import os
import re
import subprocess
import time
from pathlib import Path
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


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
    
    def generate_plan(self, user_prompt: str) -> str:
        """
        Generate a structured animation plan from user prompt.
        
        Args:
            user_prompt: Natural language description of desired animation
            
        Returns:
            Structured plan as a string with numbered steps
        """
        system_prompt = """You are an expert at planning mathematical animations for Manim (the animation engine used by 3Blue1Brown).

Given a user's description of an animation they want to create, generate a clear, detailed, step-by-step plan.

Requirements:
- Break down the animation into sequential steps
- Be specific about what mathematical objects to create (circles, squares, equations, graphs, etc.)
- Specify colors, positions, and animations (FadeIn, Transform, Write, etc.)
- Keep it concise but detailed enough for code generation
- Number each step (1., 2., 3., etc.)

Example:
User: "Show a circle transforming into a square"
Plan:
1. Create a red circle at the center of the scene
2. Display the circle with a FadeIn animation
3. Wait for 1 second
4. Create a blue square at the same position
5. Transform the circle into the square
6. Wait for 1 second before ending

Now generate a plan for the following request:"""
        
        full_prompt = f"{system_prompt}\n\nUser Request: {user_prompt}"
        
        response = self.model.generate_content(full_prompt)
        return response.text


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
    
    def generate_code(self, animation_plan: str, user_prompt: str) -> tuple[str, str]:
        """
        Generate Manim code from animation plan.
        
        Args:
            animation_plan: Structured plan with animation steps
            user_prompt: Original user prompt (for context)
            
        Returns:
            Tuple of (generated_code, class_name)
        """
        # Create unique class name based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        class_name = f"GeneratedScene_{timestamp}"
        
        system_prompt = f"""You are an expert Manim developer. Generate complete, working Python code for a Manim animation.

Requirements:
- Import statement: from manim import *
- Create a Scene class named EXACTLY: {class_name}
- Implement the construct() method with the animation
- Use proper Manim syntax and best practices
- Include comments explaining key steps
- Make sure all animations are properly sequenced with self.play() and self.wait()
- Use appropriate colors and positioning
- Keep code clean and readable

CRITICAL: The class name MUST be exactly: {class_name}

Here's the animation plan to implement:

{animation_plan}

Original user request: {user_prompt}

Generate ONLY the Python code, no explanations. Start with the import statement."""
        
        response = self.model.generate_content(system_prompt)
        generated_code = response.text
        
        # Clean up the code (remove markdown code blocks if present)
        generated_code = self._clean_code(generated_code)
        
        # Ensure the class name is correct
        generated_code = self._ensure_class_name(generated_code, class_name)
        
        # Write to file
        self.output_file.write_text(generated_code, encoding='utf-8')
        
        return generated_code, class_name
    
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


def generate_animation(user_prompt: str) -> dict:
    """
    Complete pipeline: prompt -> plan -> code -> render.
    
    Args:
        user_prompt: Natural language description of desired animation
        
    Returns:
        Dictionary with keys: success, plan, code, video_path, error, logs
    """
    result = {
        "success": False,
        "plan": "",
        "code": "",
        "class_name": "",
        "video_path": "",
        "error": "",
        "logs": ""
    }
    
    try:
        # Step 1: Generate plan
        planner = AnimationPlanner()
        plan = planner.generate_plan(user_prompt)
        result["plan"] = plan
        
        # Step 2: Generate code
        code_gen = ManimCodeGenerator()
        code, class_name = code_gen.generate_code(plan, user_prompt)
        result["code"] = code
        result["class_name"] = class_name
        
        # Step 3: Render animation
        renderer = AnimationRenderer()
        success, video_or_error, logs = renderer.render(class_name)
        result["logs"] = logs
        
        if success:
            result["success"] = True
            result["video_path"] = video_or_error
        else:
            result["error"] = video_or_error
            
    except Exception as e:
        result["error"] = f"Error in animation generation pipeline: {str(e)}"
    
    return result
