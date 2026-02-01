# 🎬 Prompt-Manim

Create beautiful mathematical animations with just natural language! Prompt-Manim transforms your text descriptions into [Manim](https://www.manim.community/) animations automatically using AI.

## ✨ Features

- 🤖 **AI-Powered**: Uses Google Gemini to understand your prompts and generate code
- 📝 **Natural Language**: Describe animations in plain English, no coding required
- 🎨 **Manim Engine**: Leverages the same animation engine used by 3Blue1Brown
- 🖥️ **Beautiful UI**: Clean Streamlit interface with real-time progress tracking
- 🎥 **Instant Preview**: View and download your animations immediately

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:

- **Python 3.11.8** (recommended version)
- **ffmpeg** - Required by Manim for video rendering
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd prompt-manim
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   
   > 🔑 **Get your API key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to generate a free Gemini API key

### Running the App

```bash
streamlit run ui/app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Enter your prompt** in the text area, describing the animation you want
2. **Click "Generate Animation"** and watch the magic happen!
3. **View your animation** in the Video tab
4. **Explore the AI's plan and code** in the other tabs
5. **Download** your animation if you're happy with it

### Example Prompts

Try these to get started:

- *"Create a blue circle that fades in and transforms into a red square"*
- *"Show the Pythagorean theorem: a² + b² = c²"*
- *"Animate a sine wave moving across the screen"*
- *"Draw a coordinate plane and plot the function f(x) = x²"*
- *"Show the number π appearing and rotating while changing colors"*

## 🏗️ Project Structure

```
prompt-manim/
├── src/
│   ├── animation_generator.py    # Core logic: LLM + Manim rendering
│   ├── generated_animations.py   # Auto-generated animation code
│   └── main.py                   # Manim examples (for reference)
├── ui/
│   └── app.py                    # Streamlit web interface
├── media/                        # Rendered videos (auto-created)
├── .env.example                  # Template for environment variables
├── requirements.txt              # Python dependencies
└── README.md                     # You are here!
```

## 🔧 How It Works

1. **Planning**: Gemini analyzes your prompt and creates a detailed animation plan
2. **Code Generation**: Gemini writes Python/Manim code based on the plan
3. **Rendering**: Manim CLI renders the animation to video (low quality for speed)
4. **Display**: The video is shown in the Streamlit interface

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure you created a `.env` file in the project root
- Check that it contains `GEMINI_API_KEY=your_key`
- Verify the API key is valid

### "Manim not found"
- Ensure you installed requirements: `pip install -r requirements.txt`
- Try reinstalling Manim: `pip install --upgrade manim`

### "ffmpeg not found"
- Install ffmpeg (see Prerequisites section)
- Make sure ffmpeg is in your system PATH
- Test by running `ffmpeg -version` in terminal

### Animation doesn't match prompt
- Try being more specific in your description
- Break complex animations into simpler steps
- Check the "Plan" tab to see how the AI interpreted your prompt

### Video not rendering
- Check the "Logs" section for detailed error messages
- Ensure you have write permissions in the project directory
- Try a simpler prompt first to verify the setup

## 🛣️ Roadmap

This is an MVP (Minimum Viable Product). Future enhancements could include:

- [ ] Support for different quality levels
- [ ] Animation history and favorites
- [ ] Edit and refine generated code
- [ ] More LLM providers (Claude, GPT-4, etc.)
- [ ] Batch generation from multiple prompts
- [ ] Community-shared animation templates

## 📄 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- [Manim Community](https://www.manim.community/) - The amazing animation engine
- [3Blue1Brown](https://www.3blue1brown.com/) - Inspiration and Manim creation
- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI-powered code generation
- [Streamlit](https://streamlit.io/) - Beautiful web interface framework

---

**Built with ❤️ for mathematical animation enthusiasts**
