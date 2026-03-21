# Relationship Affairs Prediction - ML Web Application

A production-ready Django web application that predicts the likelihood of extramarital affairs using machine learning algorithms trained on demographic and relationship data.

## 🚀 Features

- **Modern UI/UX**: Responsive design with Bootstrap 5 and custom CSS animations
- **ML Integration**: Uses scikit-learn with PCA for dimensionality reduction
- **Form Validation**: Client-side and server-side validation for all inputs
- **Error Handling**: Comprehensive error messages and fallback mechanisms
- **Sample Data**: One-click sample data for easy testing
- **Mobile Responsive**: Optimized for all screen sizes
- **Production Ready**: Updated dependencies and security configurations

## 📊 Model Overview

### Dataset
- **Source**: Affairs dataset with 6,366 records
- **Features**: 9 demographic and relationship variables
- **Target**: Number of affairs (continuous variable)

### Features Used
1. **Age** (17-50 years)
2. **Years Married** (0-30 years)
3. **Number of Children** (0-6)
4. **Education Level** (9-20 scale)
5. **Occupation Level** (1-6 scale)
6. **Marriage Rating** (1-5 scale)
7. **Religious Affiliation** (1-4 scale)
8. **Spouse's Occupation Level** (1-6 scale)

### ML Pipeline
- **Preprocessing**: One-hot encoding for categorical variables
- **Dimensionality Reduction**: Principal Component Analysis (PCA)
- **Model**: Trained regression model (pickled)
- **Prediction**: Continuous output representing predicted number of affairs

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, Bootstrap 5, Font Awesome 6
- **ML Libraries**: scikit-learn 1.3.2, pandas 2.0.3, numpy 1.24.3
- **Database**: SQLite3 (development)
- **Deployment**: Gunicorn (production-ready)

## 📋 Requirements

- Python 3.8+
- pip package manager
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd affair_prediction/mysite
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

### 4. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Development Server
```bash
python manage.py runserver
```

### 6. Access the Application
Open your browser and navigate to: `http://127.0.0.1:8000/`

## 📁 Project Structure

```
affair_prediction/
├── affairs.csv                 # Original dataset
├── Affairs.ipynb              # Jupyter notebook with ML training
└── mysite/
    ├── manage.py              # Django management script
    ├── requirements.txt       # Python dependencies
    ├── runtime.txt           # Python version specification
    ├── Procfile              # Heroku deployment configuration
    ├── mysite/               # Django project settings
    │   ├── settings.py      # Django configuration
    │   ├── urls.py          # URL routing
    │   └── wsgi.py          # WSGI configuration
    └── polls/               # Django app
        ├── views.py         # Main application logic
        ├── urls.py          # App URL routing
        ├── models.py        # Database models
        ├── templates/
        │   └── index.html   # Main UI template
        ├── Affairs.pickle   # Trained ML model
        └── AffairsPCA.pickle # PCA transformer
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the `mysite` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production Settings
For production deployment:

1. Set `DEBUG=False` in `settings.py`
2. Configure `ALLOWED_HOSTS` with your domain
3. Set a secure `SECRET_KEY`
4. Configure database settings
5. Set up static file serving

## 🧪 Testing

### Manual Testing
1. Navigate to the application
2. Click "Sample Data" to auto-fill the form
3. Click "Get Prediction" to test the ML pipeline
4. Try various input combinations to test validation

### Test Cases
- **Valid Input**: All fields filled with valid values
- **Invalid Age**: Age outside 17-50 range
- **Missing Fields**: Empty form submission
- **Edge Cases**: Minimum and maximum values for each field

## 📈 Model Performance

### Training Metrics
- **Dataset Size**: 6,366 samples
- **Features**: 9 variables (after encoding: 20+ features)
- **PCA Components**: Reduced to optimal dimensions
- **Model Type**: Regression with continuous output

### Prediction Interpretation
- **0**: No affairs predicted (very low likelihood)
- **1-2**: Low likelihood of affairs
- **3-5**: Moderate likelihood of affairs
- **6+**: High likelihood of affairs

## 🚀 Deployment

### Heroku Deployment
1. Install Heroku CLI
2. Login to Heroku: `heroku login`
3. Create app: `heroku create your-app-name`
4. Push to Heroku: `git push heroku main`

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]
```

## 🔒 Security Considerations

- Input validation and sanitization
- CSRF protection enabled
- Secure secret key management
- SQL injection prevention (Django ORM)
- XSS protection (Django templates)

## 🐛 Troubleshooting

### Common Issues

#### 1. Model Loading Error
**Problem**: `FileNotFoundError: [Errno 2] No such file or directory: 'polls/Affairs.pickle'`
**Solution**: Ensure pickle files are in the correct location: `mysite/polls/`

#### 2. Pandas Compatibility
**Problem**: `AttributeError: 'DataFrame' object has no attribute 'append'`
**Solution**: Updated to use `pd.concat()` instead of deprecated `append()`

#### 3. Django Version Conflict
**Problem**: Template rendering issues
**Solution**: Ensure all dependencies match requirements.txt versions

#### 4. Static Files Not Loading
**Problem**: CSS/JS files not found
**Solution**: Run `python manage.py collectstatic` in production

### Debug Mode
Enable debug mode in `settings.py`:
```python
DEBUG = True
```

Check Django logs for detailed error information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -m 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## 📝 License

This project is for educational and research purposes. Please ensure compliance with data privacy regulations when using real user data.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review Django and scikit-learn documentation
3. Create an issue in the repository

## 🔮 Future Enhancements

- **Model Improvement**: Feature engineering and hyperparameter tuning
- **User Authentication**: User accounts and prediction history
- **API Endpoints**: REST API for mobile app integration
- **Data Visualization**: Interactive charts and insights
- **Model Explainability**: SHAP values for feature importance
- **Multi-language Support**: Internationalization (i18n)

---

**Note**: This application is intended for educational purposes and should not be used for making real-life decisions about relationships. The predictions are based on statistical patterns and should be interpreted with caution.
