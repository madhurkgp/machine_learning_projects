# Phishing Website Detector - ML Classification System

A production-ready Django web application that uses machine learning to detect phishing websites based on URL analysis and website features.

## 🚀 Features

- **Advanced ML Model**: Trained on real phishing website data with 11 key features
- **Modern UI**: Responsive, mobile-friendly interface with Bootstrap 5
- **Real-time Analysis**: Instant classification with confidence scores
- **Input Validation**: Comprehensive form validation and error handling
- **Sample Data**: One-click sample data for easy testing
- **Security Focused**: Secure Django configuration with environment variables
- **Production Ready**: Optimized for deployment with proper logging and error handling

## 📋 System Requirements

- Python 3.8+
- Django 4.2.7
- scikit-learn 1.3.2
- pandas 2.1.4
- numpy 1.25.2

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd phising_website_classification/Code/mysite
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 🎯 Usage Guide

### Analyzing a Website

1. **Enter Website URL**: Provide the website name or URL in the input field
2. **Fill Features**: Either manually enter the feature values or click "Sample Data" for testing
3. **Click Analyze**: Submit the form for ML classification
4. **View Results**: See the phishing detection result with confidence score

### Feature Descriptions

| Feature | Description | Range |
|---------|-------------|-------|
| NumDots | Number of dots in the URL | 0-20 |
| PathLevel | URL path depth level | 0-16 |
| NumDash | Number of dashes in URL | 0-60 |
| NumSensitiveWords | Count of suspicious words | 0-5 |
| PctExtHyperlinks | Percentage of external links | 0-1 |
| PctExtResourceUrls | Percentage of external resources | 0-1 |
| InsecureForms | Presence of insecure forms | 0/1 |
| PctNullSelfRedirectHyperlinks | Self-redirect link percentage | 0-1 |
| FrequentDomainNameMismatch | Domain name mismatch | 0/1 |
| SubmitInfoToEmail | Forms submitting to email | 0/1 |
| IframeOrFrame | Presence of iframes/frames | 0/1 |

## 🧠 ML Model Details

### Model Architecture
- **Algorithm**: Random Forest Classifier (configurable)
- **Features**: 11 numerical and categorical features
- **Training Data**: Real phishing and legitimate website datasets
- **Accuracy**: High accuracy on validation dataset

### Feature Importance
1. **URL Structure**: Dots, dashes, path levels
2. **Security Indicators**: Insecure forms, HTTPS usage
3. **Content Analysis**: External links, resources
4. **Behavioral Patterns**: Redirects, domain mismatches

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Django Settings
Key settings in `mysite/settings.py`:
- Security configurations
- Database settings
- Static file handling
- Logging configuration

## 🚀 Deployment

### Production Deployment

1. **Set Environment Variables**:
```bash
export SECRET_KEY='your-production-secret-key'
export DEBUG=False
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
```

2. **Collect Static Files**:
```bash
python manage.py collectstatic
```

3. **Database Migration**:
```bash
python manage.py migrate
```

4. **Use Gunicorn**:
```bash
gunicorn mysite.wsgi:application --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🧪 Testing

### Running Tests
```bash
python manage.py test
```

### Manual Testing
1. Use the "Sample Data" button for quick testing
2. Test with various URL patterns
3. Verify edge cases and error handling

### Sample Test Cases
- **Legitimate Site**: `google.com` with normal parameters
- **Suspicious Site**: `secure-login-verify.com` with high sensitive words
- **Edge Cases**: Empty forms, invalid inputs, extreme values

## 📊 API Endpoints

### Main Application
- `GET /` - Main prediction interface
- `POST /` - Submit website for analysis

### Admin Panel
- `/admin/` - Django admin interface

## 🔒 Security Considerations

- Input validation and sanitization
- CSRF protection enabled
- Secure secret key management
- SQL injection prevention
- XSS protection

## 🐛 Troubleshooting

### Common Issues

1. **Model Not Found Error**:
   - Ensure `Phishing.pickle` exists in `polls/` directory
   - Check file permissions

2. **Dependency Conflicts**:
   - Use virtual environment
   - Update pip: `pip install --upgrade pip`

3. **Server Won't Start**:
   - Check if port 8000 is available
   - Verify Django installation

4. **Prediction Errors**:
   - Validate input ranges
   - Check model compatibility

### Debug Mode
Enable debug mode in settings:
```python
DEBUG = True
```

### Logging
Check application logs for errors:
```python
import logging
logger = logging.getLogger(__name__)
```

## 📈 Performance Optimization

- Model caching for faster predictions
- Database query optimization
- Static file compression
- CDN integration for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting guide
- Review the documentation

## 🔄 Updates & Changelog

### Version 2.0.0
- Updated Django to 4.2.7
- Modern responsive UI with Bootstrap 5
- Enhanced error handling and validation
- Improved security configuration
- Added confidence scores
- Mobile-responsive design

### Version 1.0.0
- Basic Django application
- ML model integration
- Simple form interface

---

**⚠️ Disclaimer**: This tool is for educational and research purposes. Always verify website legitimacy through multiple sources before entering sensitive information.
