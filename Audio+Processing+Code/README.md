# Audio Processing ML - Production Web Application

A sophisticated Django web application that transforms raw audio processing machine learning code into a production-ready, user-friendly platform for audio analysis and feature extraction.

## Features

### Audio Processing Capabilities
- **Time Domain Features**: Amplitude Envelope, Zero Crossing Rate, RMS Energy
- **Frequency Domain Features**: Spectral Centroid, Spectral Bandwidth, Spectral Rolloff
- **MFCC Features**: Mel-Frequency Cepstral Coefficients with derivatives
- **Advanced Analytics**: Automatic insights generation based on extracted features

### Web Application Features
- **Modern UI/UX**: Responsive design with Bootstrap 5 and custom CSS animations
- **File Upload**: Support for WAV, MP3, FLAC, M4A, OGG formats (up to 50MB)
- **Real-time Analysis**: Instant audio processing with progress indicators
- **Data Export**: Export results as JSON or CSV
- **Sample Data**: Built-in sample audio file for quick testing
- **Admin Interface**: Comprehensive Django admin for data management

## Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **Librosa 0.10.1**: Audio processing and analysis
- **NumPy 1.24.3**: Numerical computing
- **SciPy 1.11.4**: Scientific computing
- **Scikit-learn 1.3.2**: Machine learning utilities
- **SoundFile 0.12.1**: Audio file handling

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome 6.0**: Icons
- **Custom CSS**: Enhanced animations and styling
- **Chart.js**: Data visualization capabilities

### Database
- **SQLite**: Default database (configurable for PostgreSQL/MySQL)

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or Download the Project**
   ```bash
   cd "d:\project_learning\Machine_Learning\Audio+Processing+Code"
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   # Or use default: username: admin, password: admin123
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   - Main Application: http://127.0.0.1:8000
   - Admin Interface: http://127.0.0.1:8000/admin

## Usage Guide

### 1. Upload Audio File
- Navigate to the home page
- Enter a descriptive name for your audio file
- Choose an audio file (WAV, MP3, FLAC, M4A, OGG)
- Click "Upload & Analyze"

### 2. Analyze Audio
- After upload, you'll be redirected to the analysis page
- Select your uploaded file from the list
- Click "Analyze" to extract features
- Wait for processing to complete

### 3. View Results
- Analysis results display comprehensive audio features
- View time domain, frequency domain, and MFCC features
- Read AI-generated insights about your audio
- Export results in JSON or CSV format

### 4. Sample Data Testing
- Click "Load Sample Data" on the home page
- Uses the included WAV file for immediate testing
- No upload required - perfect for demonstration

## Audio Features Explained

### Time Domain Features
- **Amplitude Envelope**: Maximum amplitude value in each frame
- **Zero Crossing Rate**: Rate at which signal crosses zero axis
- **RMS Energy**: Root mean square energy indicating loudness

### Frequency Domain Features
- **Spectral Centroid**: Center of mass of the spectrum (brightness)
- **Spectral Bandwidth**: Spread of the spectrum around centroid
- **Spectral Rolloff**: Frequency below which specified percentage of energy exists

### MFCC Features
- **13 MFCC Coefficients**: Mel-frequency cepstral coefficients
- **Statistics**: Mean, standard deviation, min, and max for each coefficient
- **Applications**: Speech recognition, music genre classification

## Project Structure

```
Audio+Processing+Code/
|
|--- audio_processor/          # Django project settings
|   |--- settings.py
|   |--- urls.py
|   |--- wsgi.py
|
|--- audio_app/               # Main application
|   |--- models.py            # Database models
|   |--- views.py             # View logic
|   |--- forms.py             # Form classes
|   |--- services.py          # Audio processing service
|   |--- admin.py             # Admin configuration
|   |--- urls.py              # App URLs
|   |--- templates/           # HTML templates
|   |   |--- audio_app/
|   |       |--- base.html
|   |       |--- home.html
|   |       |--- analyze.html
|   |       |--- results.html
|
|--- static/                  # Static files
|   |--- css/
|   |   |--- custom.css       # Custom styles
|
|--- media/                   # User uploads
|   |--- audio_files/
|
|--- requirements.txt         # Python dependencies
|--- manage.py               # Django management script
|--- README.md               # This file
```

## API Endpoints

### Web Interface
- `GET /` - Home page with upload form
- `POST /upload/` - Handle audio file upload
- `GET /analyze/` - Analysis selection page
- `POST /analyze/` - Process audio analysis
- `GET /results/<id>/` - View analysis results
- `GET /load-sample/` - Load sample data (AJAX)

### Admin Interface
- `/admin/` - Django admin panel
- Manage audio files and analyses
- View system statistics

## Configuration

### Database Settings
Default configuration uses SQLite. To use PostgreSQL or MySQL:

```python
# audio_processor/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'audio_processing_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### File Upload Settings
```python
# Maximum file size (50MB default)
MAX_UPLOAD_SIZE = 50 * 1024 * 1024

# Allowed file formats
ALLOWED_AUDIO_FORMATS = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
```bash
# Check for issues
python manage.py check

# Collect static files
python manage.py collectstatic
```

### Customization
- Modify `audio_app/services.py` for new audio features
- Update templates in `audio_app/templates/` for UI changes
- Add custom CSS in `static/css/custom.css`
- Extend models in `audio_app/models.py`

## Troubleshooting

### Common Issues

1. **Import Error: librosa**
   ```bash
   pip install librosa
   ```

2. **Database Migration Issues**
   ```bash
   python manage.py makemigrations audio_app
   python manage.py migrate
   ```

3. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Audio File Upload Fails**
   - Check file size (max 50MB)
   - Verify file format (WAV, MP3, FLAC, M4A, OGG)
   - Ensure media directory permissions

5. **Analysis Processing Errors**
   - Verify audio file integrity
   - Check librosa installation
   - Review error logs in Django console

### Performance Optimization
- Use Redis for caching analysis results
- Implement background processing for large files
- Optimize database queries with select_related/prefetch_related

## Production Deployment

### Environment Variables
```bash
export DEBUG=False
export SECRET_KEY='your-secret-key'
export ALLOWED_HOSTS='yourdomain.com'
```

### Web Server Configuration
- Use Nginx or Apache as reverse proxy
- Configure Gunicorn or uWSGI for Django
- Set up SSL certificates
- Configure media file serving

### Security Considerations
- Set DEBUG=False in production
- Use environment variables for sensitive data
- Implement rate limiting for uploads
- Regular security updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and demonstration purposes. Please ensure compliance with audio file licensing terms.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Django and Librosa documentation
3. Create an issue with detailed error information

---

**Built with**: Django, Librosa, Scikit-learn, Bootstrap 5  
**Author**: ML/Django Development Team  
**Version**: 1.0.0  
**Last Updated**: 2026-04-19
