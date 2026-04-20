# Speech Analyzer - Speech Recognition & Text Analysis Platform

A production-ready Django web application that transforms audio speech into text and provides comprehensive linguistic analysis using advanced machine learning techniques.

## Features

### Core Functionality
- **Speech Recognition**: Advanced audio-to-text conversion using Google Speech Recognition API
- **Text Analysis**: Comprehensive linguistic analysis including word frequency, vocabulary diversity, and speaking patterns
- **AI Insights**: Intelligent insights about speaking speed, vocabulary usage, and communication patterns
- **Audio Processing**: Support for multiple audio formats (WAV, MP3, FLAC, M4A, OGG)

### Analysis Features
- **Word Count Analysis**: Total words, unique words, and vocabulary diversity metrics
- **Speaking Speed**: Words per minute calculation with speed categorization
- **Word Frequency**: Most frequently used words with visual representations
- **Duration Analysis**: Audio length and processing time metrics
- **Smart Insights**: AI-powered recommendations for communication improvement

### User Interface
- **Modern Design**: Responsive Bootstrap 5 interface with gradient styling
- **Interactive Charts**: Visual representations of word frequency and statistics
- **Real-time Feedback**: Progress indicators and loading animations
- **Mobile Responsive**: Optimized for all screen sizes and devices

## Technology Stack

### Backend
- **Django 4.2.7**: Web framework for robust application development
- **SpeechRecognition 3.10.0**: Audio processing and speech recognition
- **pydub 0.25.1**: Audio file manipulation and format conversion
- **pandas 2.1.3**: Data analysis and manipulation
- **numpy 1.24.3**: Numerical computing and array operations

### Frontend
- **Bootstrap 5**: Modern responsive UI framework
- **Bootstrap Icons**: Comprehensive icon library
- **Custom CSS**: Gradient styling and animations
- **JavaScript**: Interactive features and AJAX functionality

### Database
- **SQLite**: Default database for development
- **Django ORM**: Efficient database operations and relationships

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone and Navigate to Project**
   ```bash
   cd "d:\project_learning\Machine_Learning\Test+using+speech"
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser (Admin)**
   ```bash
   python manage.py createsuperuser --username admin --email admin@example.com
   # Set password as: admin123
   ```

6. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Main Application: http://127.0.0.1:8000
   - Admin Panel: http://127.0.0.1:8000/admin
     - Username: `admin`
     - Password: `admin123`

## Usage Guide

### Basic Workflow

1. **Upload Audio File**
   - Navigate to the home page
   - Click "Choose File" and select your audio file
   - Supported formats: WAV, MP3, FLAC, M4A, OGG
   - Maximum file size: 25MB

2. **Analyze Audio**
   - Click "Analyze Audio" button
   - Wait for processing (typically 10-30 seconds)
   - The system will:
     - Convert speech to text
     - Analyze word patterns
     - Calculate speaking metrics
     - Generate insights

3. **View Results**
   - **Transcribed Text**: Full audio transcription
   - **Statistics**: Word count, unique words, WPM, duration
   - **Word Frequency**: Top words with visual bars
   - **AI Insights**: Speaking speed and vocabulary analysis

4. **Manage Analyses**
   - View history of all analyses
   - Download transcriptions as text files
   - Copy text to clipboard
   - Delete unwanted analyses

### Sample Data
- Click "Try Sample" to test with pre-loaded audio
- No file upload required
- Demonstrates all features immediately

## Project Structure

```
Test+using+speech/
|
|--- speech_recognition_app/          # Django project settings
|   |--- settings.py                  # Application configuration
|   |--- urls.py                      # Main URL routing
|   |--- wsgi.py                      # WSGI deployment
|
|--- speech_analyzer/                # Main application
|   |--- models.py                    # Database models
|   |--- views.py                     # View logic
|   |--- forms.py                     # Form definitions
|   |--- services.py                  # Business logic
|   |--- urls.py                      # App URL routing
|   |--- admin.py                     # Admin interface
|   |--- templates/speech_analyzer/   # HTML templates
|   |--- migrations/                  # Database migrations
|
|--- media/                          # User uploaded files
|--- static/                         # Static assets
|--- requirements.txt                # Python dependencies
|--- README.md                      # This file
```

## API Endpoints

### Web Interface
- `GET /` - Home page with upload form
- `POST /` - Upload audio file
- `POST /analyze/<id>/` - Process audio analysis
- `GET /results/<id>/` - View analysis results
- `GET /history/` - View analysis history
- `POST /delete/<id>/` - Delete analysis
- `GET /sample-data/` - Load sample audio

### Admin Panel
- `/admin/` - Django admin interface
- Full CRUD operations for all models

## Models

### AudioAnalysis
- `audio_file`: Uploaded audio file
- `transcribed_text`: Speech-to-text result
- `word_count`: Total word count
- `unique_words`: Unique word count
- `words_per_minute`: Speaking speed
- `audio_duration`: Audio length in minutes
- `created_at`: Timestamp

### WordFrequency
- `audio_analysis`: Related analysis
- `word`: The word
- `frequency`: Count of occurrences

## Configuration

### Environment Variables
The application uses Django settings by default. For production, consider:

1. **Security Settings**
   ```python
   SECRET_KEY = 'your-secret-key'
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. **Database Configuration**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'speech_analyzer',
           'USER': 'username',
           'PASSWORD': 'password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Media Files**
   ```python
   MEDIA_ROOT = '/path/to/media/files'
   MEDIA_URL = '/media/'
   ```

## Troubleshooting

### Common Issues

1. **FFmpeg Warning**
   - **Issue**: Warning about FFmpeg not found
   - **Solution**: Install FFmpeg for full audio format support
   - **Impact**: Basic functionality still works without FFmpeg

2. **Speech Recognition Fails**
   - **Issue**: "Could not transcribe audio" error
   - **Solutions**:
     - Check audio quality and clarity
     - Ensure supported audio format
     - Verify internet connection (Google API)
     - Try shorter audio segments

3. **File Upload Issues**
   - **Issue**: File not uploading
   - **Solutions**:
     - Check file size (max 25MB)
     - Verify supported format
     - Ensure proper file permissions

4. **Server Issues**
   - **Issue**: Server won't start
   - **Solutions**:
     - Check virtual environment activation
     - Verify all dependencies installed
     - Check port 8000 availability

### Performance Optimization

1. **Large Audio Files**
   - Consider chunking large files
   - Implement progress indicators
   - Use background processing for very large files

2. **Database Optimization**
   - Add indexes to frequently queried fields
   - Implement database connection pooling
   - Use Redis for caching frequent queries

## Development

### Adding New Features

1. **New Analysis Types**
   - Extend `SpeechAnalyzerService` class
   - Add new model fields
   - Update templates and views

2. **Additional Audio Formats**
   - Update form validators
   - Modify service processing
   - Test new formats thoroughly

3. **Enhanced UI Features**
   - Add new template files
   - Extend CSS styling
   - Implement new JavaScript features

### Testing

1. **Unit Tests**
   ```bash
   python manage.py test
   ```

2. **Manual Testing Checklist**
   - File upload with various formats
   - Analysis processing and results
   - Error handling and edge cases
   - Mobile responsiveness
   - Admin interface functionality

## Production Deployment

### Deployment Checklist

1. **Security**
   - Set strong SECRET_KEY
   - Disable DEBUG mode
   - Configure ALLOWED_HOSTS
   - Set up HTTPS
   - Implement rate limiting

2. **Performance**
   - Configure production database
   - Set up static file serving
   - Implement caching
   - Configure monitoring

3. **Scalability**
   - Load balancing setup
   - Database replication
   - CDN for static assets
   - Background task processing

### Docker Deployment

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with proper testing
4. Submit pull request
5. Follow coding standards

## License

This project is for educational and demonstration purposes. Please ensure compliance with:
- Google Speech Recognition API terms
- Audio file usage rights
- Data privacy regulations

## Support

For issues and questions:
1. Check troubleshooting section
2. Review Django documentation
3. Consult SpeechRecognition library docs
4. Verify audio file compatibility

## Version History

- **v1.0.0**: Initial release with core functionality
  - Speech recognition integration
  - Text analysis features
  - Modern responsive UI
  - Admin interface
  - Sample data functionality

---

**Note**: This application demonstrates the complete ML-to-production pipeline, transforming raw audio processing notebooks into a professional web application with modern UI/UX design and comprehensive functionality.
