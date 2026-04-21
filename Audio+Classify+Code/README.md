# Audio Classification System

A production-ready web application for classifying audio files using neural networks and the UrbanSound8K dataset. This system transforms raw ML models into a professional Django web application with modern UI/UX design.

## 🎯 Features

### Core Functionality
- **Audio Classification**: Classify audio files into 10 urban sound categories
- **Neural Network Model**: Deep learning architecture with MFCC feature extraction
- **Real-time Processing**: Fast audio analysis and classification
- **Multiple Formats**: Support for WAV, MP3, FLAC, M4A, OGG formats
- **File Upload**: Drag-and-drop interface with validation

### User Interface
- **Modern Design**: Bootstrap 5 with custom CSS animations
- **Responsive Layout**: Mobile-friendly interface
- **Interactive Dashboard**: Real-time classification results
- **Progress Tracking**: Visual feedback during processing
- **History Management**: View and manage classification history

### Technical Features
- **REST API**: Programmatic access to classification
- **Data Export**: Download results in JSON format
- **Sample Data**: Pre-loaded samples for testing
- **Admin Panel**: Django admin for data management
- **Error Handling**: Comprehensive error management

## 🏗️ Architecture

### ML Pipeline
1. **Audio Processing**: Librosa for audio feature extraction
2. **Feature Engineering**: MFCC (10 coefficients) and Zero Crossing Rate
3. **Neural Network**: Sequential model with dropout layers
4. **Classification**: 10-class urban sound classification

### Web Application
- **Backend**: Django 4.2.7 with custom services
- **Frontend**: Bootstrap 5 with custom CSS
- **Database**: SQLite (configurable for PostgreSQL/MySQL)
- **File Storage**: Django media handling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone and Setup**
   ```bash
   cd "d:\project_learning\Machine_Learning\Audio+Classify+Code"
   python -m venv venv
   venv\Scripts\activate
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
   ```

5. **Run Server**
   ```bash
   python manage.py runserver
   ```

6. **Access Application**
   - Main App: http://127.0.0.1:8000
   - Admin Panel: http://127.0.0.1:8000/admin

## 📊 Supported Audio Classes

| Class | Description | Icon |
|-------|-------------|------|
| Air Conditioner | Mechanical cooling sounds | 🌬️ |
| Car Horn | Vehicle warning sounds | 📢 |
| Children Playing | Kids playing sounds | 👥 |
| Dog Bark | Canine vocalizations | 🐕 |
| Drilling | Construction sounds | 🔧 |
| Engine Idling | Vehicle engine sounds | ⚙️ |
| Gun Shot | Firearm discharge sounds | 🔫 |
| Jackhammer | Heavy machinery | 🔨 |
| Siren | Emergency vehicle sounds | 🚨 |
| Street Music | Musical performances | 🎵 |

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
For production, update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'audio_classification',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### File Upload Settings
```python
# Maximum file size (25MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024

# Allowed extensions
ALLOWED_AUDIO_EXTENSIONS = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
```

## 📡 API Documentation

### Classify Audio
**Endpoint**: `POST /api/classify/`

**Request**:
- Content-Type: `multipart/form-data`
- Field: `audio_file` (audio file)

**Response**:
```json
{
    "success": true,
    "predicted_class": "dog_bark",
    "confidence_score": 0.8473,
    "class_probabilities": [
        {"class_name": "dog_bark", "probability": 0.8473},
        {"class_name": "car_horn", "probability": 0.0521},
        ...
    ],
    "processing_time": 0.234
}
```

### Error Response
```json
{
    "success": false,
    "error": "File type not supported"
}
```

## 🎨 UI Features

### Home Page
- Drag-and-drop file upload
- Recent classifications display
- Supported classes overview
- Quick access to sample data

### Results Page
- Detailed classification results
- Confidence scores with visual indicators
- All class probabilities
- Audio player for uploaded files
- Download results functionality

### History Page
- Paginated classification history
- Search and filter capabilities
- Export functionality
- Performance statistics

### Sample Data
- Pre-loaded audio samples
- Dataset information
- Class descriptions
- Quick testing interface

## 🔍 Model Details

### Neural Network Architecture
```
Input Layer (10 features) → Dense(100) → ReLU → Dropout(0.5)
→ Dense(200) → ReLU → Dropout(0.5) → Dense(100) → ReLU → Dropout(0.5)
→ Dense(10) → Sigmoid → Output
```

### Feature Extraction
- **MFCC**: 10 Mel-frequency cepstral coefficients
- **ZCR**: Zero crossing rate (average)
- **Duration**: Audio length in seconds
- **Sample Rate**: 44.1 kHz processing

### Training Dataset
- **Source**: UrbanSound8K dataset
- **Size**: 8,732 audio files
- **Classes**: 10 urban sound categories
- **Duration**: ≤4 seconds per file

## 🛠️ Development

### Project Structure
```
Audio+Classify+Code/
├── audio_classification_project/     # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── audio_classifier/               # Django app
│   ├── models.py                   # Database models
│   ├── views.py                    # View logic
│   ├── forms.py                    # Forms
│   ├── services.py                 # ML services
│   ├── admin.py                    # Admin configuration
│   ├── urls.py                     # App URLs
│   └── templates/                  # HTML templates
├── static/                         # Static files
│   ├── css/custom.css
│   └── js/
├── media/                          # User uploads
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

### Adding New Features
1. **New Audio Classes**: Update `CLASSES` in `services.py`
2. **Custom Models**: Modify `AudioClassificationService`
3. **UI Changes**: Update templates and CSS
4. **API Endpoints**: Add views and URL patterns

### Testing
```bash
# Run tests
python manage.py test

# Test specific app
python manage.py test audio_classifier

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Production Settings
1. **Set DEBUG=False** in settings
2. **Configure ALLOWED_HOSTS**
3. **Set up production database**
4. **Configure static file serving**
5. **Set up SSL/TLS**

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "audio_classification_project.wsgi:application"]
```

### Environment Setup
```bash
# Production dependencies
pip install gunicorn psycopg2-binary

# Static files
python manage.py collectstatic

# Database migrations
python manage.py migrate
```

## 🔧 Troubleshooting

### Common Issues

**File Upload Errors**
- Check file size limit (25MB)
- Verify file format support
- Ensure media directory permissions

**Model Loading Issues**
- Verify TensorFlow installation
- Check model file paths
- Ensure proper dependencies

**Database Errors**
- Run migrations: `python manage.py migrate`
- Check database connection settings
- Verify database permissions

**Performance Issues**
- Optimize audio file sizes
- Consider async processing
- Monitor memory usage

### Debug Mode
Enable debug logging in settings:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## 📈 Performance

### Benchmarks
- **Average Processing Time**: 0.2-0.5 seconds
- **Memory Usage**: ~100MB per classification
- **File Size Limit**: 25MB
- **Supported Formats**: 5 audio formats

### Optimization Tips
- Use compressed audio files
- Implement caching for repeated classifications
- Consider batch processing for multiple files
- Monitor system resources

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Code review and merge

### Code Standards
- Follow PEP 8 guidelines
- Add docstrings to functions
- Include type hints
- Write comprehensive tests

## 📄 License

This project is for educational and research purposes. The UrbanSound8K dataset has its own licensing terms.

## 🙏 Acknowledgments

- **UrbanSound8K Dataset**: Provided by Cornell University
- **Librosa**: Audio processing library
- **TensorFlow**: Machine learning framework
- **Django**: Web framework
- **Bootstrap**: UI framework

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the documentation
3. Check GitHub issues
4. Contact the development team

---

**Quick Links**:
- [Live Demo](http://127.0.0.1:8000)
- [Admin Panel](http://127.0.0.1:8000/admin)
- [API Documentation](#api-documentation)
- [Dataset Info](#-supported-audio-classes)

**Version**: 1.0.0  
**Last Updated**: 2024  
**Framework**: Django 4.2.7 + TensorFlow 2.13.0
