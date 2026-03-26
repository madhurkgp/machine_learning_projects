#!/usr/bin/env python
"""
Medical Cost Prediction Application Setup Script
This script helps set up the development environment and runs the application.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"🔄 {description}")
    print(f"{'='*50}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {description}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description}")
        print(f"Error message: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: Python {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible.")
        return True

def check_virtual_env():
    """Check if running in virtual environment."""
    print("🔍 Checking virtual environment...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment.")
        return True
    else:
        print("⚠️  Not running in virtual environment. Consider using one for better dependency management.")
        return False

def install_dependencies():
    """Install required packages."""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def run_django_checks():
    """Run Django system checks."""
    return run_command("python manage.py check", "Running Django system checks")

def run_migrations():
    """Apply Django migrations."""
    return run_command("python manage.py migrate", "Applying database migrations")

def start_server():
    """Start the Django development server."""
    print("\n" + "="*50)
    print("🚀 Starting Django Development Server")
    print("="*50)
    print("Server will be available at: http://127.0.0.1:8000/")
    print("Press Ctrl+C to stop the server")
    print("="*50)
    
    try:
        subprocess.run("python manage.py runserver", shell=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")

def main():
    """Main setup function."""
    print("🏥 Medical Cost Prediction Application Setup")
    print("="*50)
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mysite_dir = os.path.join(script_dir, 'mysite')
    
    if os.path.exists(mysite_dir):
        os.chdir(mysite_dir)
        print(f"📁 Changed to directory: {mysite_dir}")
    else:
        print(f"❌ Directory not found: {mysite_dir}")
        return False
    
    # Run setup steps
    steps = [
        ("Python Version Check", check_python_version),
        ("Virtual Environment Check", check_virtual_env),
        ("Install Dependencies", install_dependencies),
        ("Django System Check", run_django_checks),
        ("Apply Migrations", run_migrations),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the above errors and try again.")
            return False
    
    print("\n🎉 Setup completed successfully!")
    
    # Ask user if they want to start the server
    try:
        response = input("\nWould you like to start the development server now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            start_server()
        else:
            print("\n💡 To start the server manually, run:")
            print("   python manage.py runserver")
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")
    
    return True

if __name__ == "__main__":
    main()
