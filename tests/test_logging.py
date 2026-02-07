"""
Test script for console logging

This script tests the animation generator with console logging.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from animation_generator import generate_animation

def main():
    print("=" * 60)
    print("Testing Animation Generator with Console Logging")
    print("=" * 60)
    print()
    
    # Test prompt
    prompt = "Create a blue circle that transforms into a red square"
    
    # Generate with default logger (prints to console)
    result = generate_animation(prompt)
    
    print()
    print("=" * 60)
    print("Generation Complete")
    print("=" * 60)
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Video: {result['video_path']}")
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    main()
