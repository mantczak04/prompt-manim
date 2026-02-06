"""
Prompt-Manim Streamlit UI

A simple interface for generating Manim animations from natural language prompts.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from animation_generator import generate_animation


# Page configuration
st.set_page_config(
    page_title="Prompt-Manim",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎬 Prompt-Manim</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Create beautiful mathematical animations with natural language</div>', unsafe_allow_html=True)

# Sidebar with info and examples
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **Prompt-Manim** transforms your text descriptions into Manim animations automatically!
    
    **How it works:**
    1. Describe your animation in plain English
    2. AI creates a detailed animation plan
    3. AI generates Manim Python code
    4. Video renders and displays automatically
    """)
    
    st.divider()
    
    st.header("✨ Example Prompts")
    
    examples = [
        "Create a blue circle that fades in and transforms into a red square",
        "Show the Pythagorean theorem: a² + b² = c²",
        "Animate a sine wave moving across the screen",
        "Draw a coordinate plane and plot the function f(x) = x²",
        "Show the number π appearing and rotating while changing colors"
    ]
    
    for example in examples:
        if st.button(example, key=f"example_{example[:20]}", use_container_width=True):
            st.session_state.prompt = example
    
    st.divider()
    
    st.header("⚙️ Settings")
    st.caption("Quality: Low (for speed)")
    st.caption("Model: Gemini Pro")

# Main content area
st.header("🎨 Create Your Animation")

# Input section
prompt = st.text_area(
    "Describe the animation you want to create:",
    height=100,
    placeholder="Example: Create a circle that transforms into a square...",
    value=st.session_state.get("prompt", ""),
    key="prompt_input"
)

# Update session state
if prompt:
    st.session_state.prompt = prompt

# Generate button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    generate_button = st.button("🎬 Generate Animation", type="primary", use_container_width=True)

# Generation logic
if generate_button:
    if not prompt:
        st.error("⚠️ Please enter a description of your animation!")
    else:
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Planning
        status_text.text("🤔 Step 1/3: Creating animation plan...")
        progress_bar.progress(10)
        
        with st.spinner("Thinking..."):
            result = generate_animation(prompt)
        
        if result.get("plan"):
            progress_bar.progress(33)
            status_text.text("✅ Step 1/3: Plan created!")
        
        # Step 2: Code Generation  
        if result.get("code"):
            status_text.text("💻 Step 2/3: Generating Manim code...")
            progress_bar.progress(50)
            
            import time
            time.sleep(0.5)  # Brief pause for UX
            
            progress_bar.progress(66)
            status_text.text("✅ Step 2/3: Code generated!")
        
        # Step 3: Rendering
        if result.get("code"):
            status_text.text("🎥 Step 3/3: Rendering animation...")
            progress_bar.progress(75)
            
        # Complete
        progress_bar.progress(100)
        
        if result["success"]:
            status_text.text("✅ Animation complete!")
            
            # Success message
            st.markdown('<div class="success-box">✅ <b>Animation generated successfully!</b></div>', unsafe_allow_html=True)
            
            # Display results in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["🎥 Video", "📋 Plan", "💻 Code", "📊 Token Usage"])
            
            with tab1:
                st.subheader("Generated Animation")
                
                video_path = Path(result["video_path"])
                if video_path.exists():
                    st.video(str(video_path))
                    
                    # Download button
                    with open(video_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Video",
                            data=f,
                            file_name=f"animation_{result['class_name']}.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("Video file not found")
            
            with tab2:
                st.subheader("Animation Plan")
                st.text(result["plan"])
            
            with tab3:
                st.subheader("Generated Manim Code")
                st.code(result["code"], language="python")
                
                # Show logs in expander
                if result.get("logs"):
                    with st.expander("📊 Rendering Logs"):
                        st.text(result["logs"])
            
            with tab4:
                st.subheader("Token Usage & Cost")
                
                token_data = result.get("token_usage", {})
                
                # Overview metrics in columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        label="Total Input Tokens",
                        value=f"{token_data.get('total_input_tokens', 0):,}"
                    )
                
                with col2:
                    st.metric(
                        label="Total Output Tokens",
                        value=f"{token_data.get('total_output_tokens', 0):,}"
                    )
                
                with col3:
                    total_cost = token_data.get('total_cost_usd', 0)
                    st.metric(
                        label="Total Cost",
                        value=f"${total_cost:.6f} USD"
                    )
                
                st.divider()
                
                # Detailed breakdown
                st.subheader("Detailed Breakdown")
                
                # Planning step
                st.write("**Step 1: Animation Planning**")
                plan_col1, plan_col2 = st.columns(2)
                with plan_col1:
                    st.write(f"- Input tokens: **{token_data.get('plan_input_tokens', 0):,}**")
                with plan_col2:
                    st.write(f"- Output tokens: **{token_data.get('plan_output_tokens', 0):,}**")
                
                # Code generation step
                st.write("**Step 2: Code Generation**")
                code_col1, code_col2 = st.columns(2)
                with code_col1:
                    st.write(f"- Input tokens: **{token_data.get('code_input_tokens', 0):,}**")
                with code_col2:
                    st.write(f"- Output tokens: **{token_data.get('code_output_tokens', 0):,}**")
                
                st.divider()
                
                # Cost breakdown
                st.subheader("Cost Breakdown")
                st.write("**Pricing (Gemini 3 Flash Preview):**")
                st.write("- Input: $0.50 per 1M tokens")
                st.write("- Output: $3.00 per 1M tokens")
                
                st.write("")
                st.write("**Your costs:**")
                input_cost = token_data.get('input_cost_usd', 0)
                output_cost = token_data.get('output_cost_usd', 0)
                st.write(f"- Input cost: **${input_cost:.6f}** ({token_data.get('total_input_tokens', 0):,} tokens)")
                st.write(f"- Output cost: **${output_cost:.6f}** ({token_data.get('total_output_tokens', 0):,} tokens)")
                st.write(f"- **Total: ${total_cost:.6f}**")
        
        else:
            # Error handling
            status_text.text("❌ Generation failed")
            
            error_msg = result.get("error", "Unknown error occurred")
            st.markdown(f'<div class="error-box">❌ <b>Error:</b> {error_msg}</div>', unsafe_allow_html=True)
            
            # Show what we have so far
            if result.get("plan"):
                with st.expander("📋 View Generated Plan"):
                    st.text(result["plan"])
            
            if result.get("code"):
                with st.expander("💻 View Generated Code"):
                    st.code(result["code"], language="python")
            
            if result.get("logs"):
                with st.expander("📊 View Logs"):
                    st.text(result["logs"])
            
            # Helpful suggestions
            st.info("""
            **Troubleshooting Tips:**
            - Make sure your GEMINI_API_KEY is set correctly in .env
            - Ensure Manim is installed: `pip install manim`
            - Check that ffmpeg is installed and in your PATH
            - Try simplifying your prompt
            """)

# Footer
st.divider()
st.caption("Built with ❤️ using Manim, Streamlit, and Gemini AI")
