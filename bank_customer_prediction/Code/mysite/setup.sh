#!/bin/bash

echo "Setting up Bank Credit Card Prediction ML Application..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Start the development server
echo
echo "Setup complete! Starting the development server..."
echo
echo "The application will be available at: http://127.0.0.1:8000"
echo
echo "Press Ctrl+C to stop the server"
echo

python manage.py runserver
