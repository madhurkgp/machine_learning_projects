# Clothing Fit Predictor - ML Powered Quality Assessment

A production-ready Django web application that uses machine learning to predict clothing fit quality based on user measurements and preferences.

## 🚀 Features

- **ML-Powered Predictions**: Uses Random Forest classifier trained on 82,790 clothing reviews
- **Modern UI**: Responsive, gradient-based design with smooth animations
- **Input Validation**: Comprehensive form validation with user-friendly error messages
- **Sample Data**: One-click sample data for easy testing
- **Quality Scoring**: Predicts clothing quality on a scale of 1-5 with actionable recommendations
- **Mobile Responsive**: Fully responsive design that works on all devices

## 📊 ML Model Details

- **Algorithm**: Random Forest Classifier (250 estimators)
- **Training Accuracy**: 95.82%
- **Test Accuracy**: 43.07%
- **Features**: 9 input parameters including size, measurements, and preferences
- **Target Variable**: Quality rating (1-5 scale)
- **Training Dataset**: 82,790 clothing reviews with measurements

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, JavaScript (no external frameworks)
- **ML Library**: Scikit-learn 1.3.2
- **Data Processing**: Pandas 2.0.3, NumPy 1.24.3
- **Database**: SQLite3 (development)

## 📋 Input Features

The model uses the following input parameters:

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| Size | Numeric | 0-50 | Garment size number |
| Cup Size | Categorical | 0-11 | A, AA, B, C, D, DD/E, DDD/F, DDDD/G, H, I, J, K |
| Bra Size | Numeric | 28-44 | Band size in inches |
| Category | Categorical | 0-6 | Bottoms, Dresses, New, Outerwear, Sale, Tops, Wedding |
| Length | Categorical | 0-5 | Just Right, Slightly Long, Lightly Short, Slightly Short, Very Long, Very Short |
| Fit | Categorical | 0-2 | Fit, Large, Small |
| Shoe Size | Numeric | 4-15 | Shoe size (includes half sizes) |
| Shoe Width | Categorical | 0-2 | Average, Narrow, Wide |
| Height | Numeric | 48-84 | Height in inches |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cloth_fit_prediction/mysite
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

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000/`

## 🧪 Testing the Application

### Using Sample Data

Click the "Sample Data" button to automatically fill the form with test values:
- Name: Jane Doe
- Size: 8
- Height: 65 inches
- Cup Size: C
- Bra Size: 34
- Category: Tops
- Length: Just Right
- Fit: Fit
- Shoe Size: 8
- Shoe Width: Average

### Manual Testing

1. Fill in all required fields with valid values
2. Click "Predict Quality" to get a quality score (1-5)
3. Review the recommendation based on the score

### Edge Cases to Test

- Invalid input values (negative numbers, text in numeric fields)
- Missing required fields
- Boundary values (minimum/maximum sizes)
- Empty form submission

## 📁 Project Structure

```
cloth_fit_prediction/
├── mysite/
│   ├── manage.py                 # Django management script
│   ├── requirements.txt          # Python dependencies
│   ├── runtime.txt              # Python version specification
│   ├── Procfile                 # Heroku deployment configuration
│   ├── db.sqlite3               # SQLite database
│   ├── mysite/                  # Django project configuration
│   │   ├── __init__.py
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # Main URL configuration
│   │   ├── wsgi.py              # WSGI configuration
│   │   └── asgi.py              # ASGI configuration
│   └── polls/                   # Django app
│       ├── __init__.py
│       ├── admin.py             # Django admin configuration
│       ├── apps.py              # App configuration
│       ├── models.py            # Database models
│       ├── views.py             # View logic and ML integration
│       ├── urls.py              # App URL configuration
│       ├── Clothes.pickle       # Trained ML model
│       └── templates/
│           └── index.html       # Main HTML template
├── clothing.ipynb               # Jupyter notebook with ML training
├── cloth_yelp.json              # Training dataset
└── README.md                    # This file
```

## 🔧 Configuration

### Development Settings

The application is configured for development with:
- `DEBUG = True` for detailed error messages
- `ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0']` for local access
- SQLite database for easy setup

### Production Settings

For production deployment:
1. Set `DEBUG = False`
2. Update `ALLOWED_HOSTS` with your domain
3. Configure proper database (PostgreSQL recommended)
4. Set up static files serving
5. Configure environment variables for sensitive data

## 🚀 Deployment

### Heroku Deployment

1. Install Heroku CLI
2. Login to Heroku: `heroku login`
3. Create app: `heroku create your-app-name`
4. Push to Heroku: `git push heroku main`

The `Procfile` and `runtime.txt` are already configured for Heroku deployment.

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t clothing-fit-predictor .
docker run -p 8000:8000 clothing-fit-predictor
```

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Error**
   - Ensure `Clothes.pickle` exists in `polls/` directory
   - Check file permissions

2. **Dependency Conflicts**
   - Use the exact versions in `requirements.txt`
   - Create a fresh virtual environment

3. **Django Server Issues**
   - Check if port 8000 is available
   - Try `python manage.py runserver 8001`

4. **Prediction Errors**
   - Verify all input fields are filled
   - Check input value ranges
   - Review server logs for detailed errors

### Debug Mode

Enable debug mode by setting `DEBUG = True` in `settings.py` to see detailed error messages.

## 📈 Model Performance

The Random Forest model shows:
- **High training accuracy** (95.82%) indicates good fit to training data
- **Moderate test accuracy** (43.07%) suggests room for improvement
- **Feature importance**: Size and measurements have highest predictive power

### Potential Improvements

1. **Feature Engineering**: Add derived features like BMI
2. **Model Tuning**: Hyperparameter optimization
3. **Ensemble Methods**: Combine multiple models
4. **More Data**: Increase training dataset size
5. **Cross-validation**: Better evaluation methodology

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -m "Add feature description"`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is for educational purposes. Please ensure compliance with dataset licenses and terms of use.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the error logs
3. Create an issue with detailed description
4. Include steps to reproduce the problem

## 🔄 Version History

- **v1.0.0**: Initial production-ready version
  - Modern UI with responsive design
  - Enhanced error handling and validation
  - Updated dependencies for compatibility
  - Comprehensive documentation

---

**Note**: This application uses a trained machine learning model for predictions. The accuracy depends on the quality and diversity of training data. Results should be used as recommendations rather than definitive assessments.
