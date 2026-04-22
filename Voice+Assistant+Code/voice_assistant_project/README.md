# Voice Assistant Dave - Production Ready Web Application

A sophisticated voice assistant web application built with Django that transforms voice commands into intelligent actions. Dave can search Wikipedia, open websites, tell time, check weather, and much more through a beautiful, modern interface.

## 🚀 Features

### Core Functionality
- **Voice Recognition**: Convert speech to text using Google Speech Recognition API
- **Text-to-Speech**: Natural voice responses using pyttsx3
- **Command Processing**: Intelligent parsing and execution of voice commands
- **Web Integration**: Open popular websites instantly (YouTube, Google, Instagram, etc.)
- **Wikipedia Search**: Get instant information from Wikipedia
- **Time & Weather**: Real-time information queries
- **Command History**: Track all interactions with detailed analytics

### User Interface
- **Modern Responsive Design**: Built with Bootstrap 5 and custom CSS gradients
- **Glass Morphism UI**: Beautiful frosted glass effect with smooth animations
- **Mobile Friendly**: Fully responsive design for all devices
- **Interactive Dashboard**: Real-time feedback and status indicators
- **Command Suggestions**: Quick access to available commands
- **Dark Theme**: Easy on the eyes with professional aesthetics

### Analytics & Management
- **Usage Analytics**: Track command patterns and performance metrics
- **Response Time Monitoring**: Measure assistant performance
- **Success Rate Tracking**: Monitor command execution success
- **Django Admin Interface**: Comprehensive data management
- **Export Functionality**: Download interaction history

## 🛠️ Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **Python 3.10+**: Programming language
- **SQLite**: Database (configurable for PostgreSQL/MySQL)
- **SpeechRecognition 3.10.0**: Voice-to-text conversion
- **pyttsx3 2.90**: Text-to-speech synthesis
- **Wikipedia 1.4.0**: Wikipedia API integration

### Frontend
- **Bootstrap 5.3.0**: Responsive UI framework
- **Bootstrap Icons**: Icon library
- **Custom CSS**: Glass morphism effects and animations
- **JavaScript**: Interactive functionality and AJAX requests

### Deployment
- **Gunicorn 21.2.0**: WSGI server
- **Whitenoise 6.6.0**: Static file serving

## 📋 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| Wikipedia Search | Search Wikipedia for information | "wikipedia Albert Einstein" |
| Open YouTube | Launch YouTube website | "open youtube" |
| Open Google | Launch Google search | "open google" |
| Open Instagram | Launch Instagram | "open instagram" |
| Check Weather | Open weather website | "the weather" |
| Check Scores | Open cricket scores | "the score" |
| Get Time | Tell current time | "the time" |
| Play Music | Play music files | "play music" |

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd voice_assistant_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   # Or use default: admin/admin123
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000
   - Admin interface: http://127.0.0.1:8000/admin

## 🎯 Usage Guide

### Using the Voice Assistant

1. **Text Input**: Type your command in the input field and press Enter or click Send
2. **Voice Input**: Click the microphone button and speak your command clearly
3. **Command Suggestions**: Click on suggested commands for quick access
4. **View Responses**: See assistant responses with execution details
5. **Track History**: Navigate to History to see all past interactions

### Voice Recognition Tips

- **Microphone Access**: Allow browser microphone permissions when prompted
- **Clear Speech**: Speak clearly and at a moderate pace
- **Quiet Environment**: Minimize background noise for better accuracy
- **Exact Phrases**: Use the exact command phrases listed above
- **Fallback**: If voice doesn't work, use text input instead

### Analytics Dashboard

- **Performance Metrics**: View response times and success rates
- **Command Distribution**: See which commands are used most
- **Recent Activity**: Monitor latest interactions
- **System Health**: Check overall application status

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Database Configuration

For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'voice_assistant',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Speech Recognition Settings

Configure speech recognition in `voice_assistant/services.py`:

```python
# Adjust recognition settings
self.recognizer.dynamic_energy_threshold = True
self.recognizer.pause_threshold = 0.8
```

## 🚀 Deployment

### Production Deployment with Gunicorn

1. **Install production dependencies**
   ```bash
   pip install gunicorn whitenoise
   ```

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn voice_assistant_project.wsgi:application --bind 0.0.0.0:8000
   ```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "voice_assistant_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Heroku Deployment

1. **Create Procfile**
   ```
   web: gunicorn voice_assistant_project.wsgi:application --bind 0.0.0.0:$PORT
   ```

2. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku run python manage.py migrate
   ```

## 🐛 Troubleshooting

### Common Issues

1. **Microphone Not Working**
   - Check browser microphone permissions
   - Ensure microphone is connected and not muted
   - Try refreshing the page

2. **Speech Recognition Errors**
   - Speak more clearly and slowly
   - Check internet connection for Google Speech API
   - Try using text input as fallback

3. **Slow Response Times**
   - Check internet connection speed
   - Close other browser tabs
   - Some commands (Wikipedia) naturally take longer

4. **Server Won't Start**
   - Check if port 8000 is available
   - Ensure all dependencies are installed
   - Check Django settings for errors

### Debug Mode

Enable debug logging in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'voice_assistant': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add feature description'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Django Team** - Excellent web framework
- **SpeechRecognition Library** - Voice-to-text conversion
- **pyttsx3** - Text-to-speech synthesis
- **Bootstrap** - Responsive UI framework
- **Wikipedia API** - Information source

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

---

**Voice Assistant Dave** - Your intelligent AI companion for voice commands and web automation. Built with ❤️ using Django and modern web technologies.
