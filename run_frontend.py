#!/usr/bin/env python3
"""
Frontend Development Server for UrbanEase
Run this script to start the Django development server for testing the frontend.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Change to project directory
    os.chdir(project_root)
    
    print("🚀 Starting UrbanEase Frontend Development Server...")
    print("=" * 50)
    
    # Check if virtual environment exists
    venv_path = project_root / "venv"
    if venv_path.exists():
        print("✅ Virtual environment found")
        
        # Activate virtual environment and run server
        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"
        
        if python_path.exists():
            print(f"🐍 Using Python: {python_path}")
            subprocess.run([str(python_path), "manage.py", "runserver", "0.0.0.0:8000"])
        else:
            print("❌ Python executable not found in virtual environment")
            print("Please create a virtual environment first:")
            print("python -m venv venv")
            print("source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
            print("pip install -r requirements.txt")
    else:
        print("❌ Virtual environment not found")
        print("Please create a virtual environment first:")
        print("python -m venv venv")
        print("source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("pip install -r requirements.txt")
        print("\nThen run this script again.")

if __name__ == "__main__":
    main() 