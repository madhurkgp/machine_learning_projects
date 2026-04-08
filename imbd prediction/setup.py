#!/usr/bin/env python
"""
Setup script for IMDB Rating Predictor
This script sets up the project from scratch including:
- Virtual environment creation
- Dependency installation
- Model training
- Database migrations
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("SUCCESS!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    """Main setup function"""
    print("IMDB Rating Predictor Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    
    # Commands to run
    setup_commands = [
        ("python -m venv venv", "Creating virtual environment"),
        ("venv\\Scripts\\activate && pip install --upgrade pip", "Upgrading pip"),
        ("venv\\Scripts\\activate && pip install -r requirements.txt", "Installing dependencies"),
        ("python prediction/ml_model.py", "Training ML model"),
        ("python manage.py makemigrations", "Creating migrations"),
        ("python manage.py migrate", "Applying migrations"),
        ("python manage.py collectstatic --noinput", "Collecting static files"),
    ]
    
    success_count = 0
    
    for command, description in setup_commands:
        if run_command(command, description):
            success_count += 1
        else:
            print(f"Failed to: {description}")
            print("Please check the error above and try manually.")
            return False
    
    print(f"\n{'='*50}")
    print(f"Setup Complete! {success_count}/{len(setup_commands)} tasks completed successfully.")
    print('='*50)
    
    if success_count == len(setup_commands):
        print("\nTo run the application:")
        print("1. Activate virtual environment: venv\\Scripts\\activate")
        print("2. Start server: python manage.py runserver")
        print("3. Open browser: http://127.0.0.1:8000")
        return True
    else:
        print("\nSome setup steps failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    main()
