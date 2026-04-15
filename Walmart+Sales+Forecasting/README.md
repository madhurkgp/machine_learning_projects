# Walmart Sales Forecasting - ML Web Application

A production-ready Django web application that predicts weekly Walmart store sales using machine learning algorithms (Ridge and Lasso Regression).

## 🚀 Features

- **ML-Powered Predictions**: Uses trained Ridge and Lasso regression models
- **Modern Responsive UI**: Built with Bootstrap 5 and custom CSS
- **Real-time Forecasting**: Instant sales predictions with confidence scores
- **Interactive Dashboard**: View prediction history and analytics
- **REST API**: Programmatic access to prediction endpoints
- **Sample Data**: Easy testing with pre-loaded sample data
- **Mobile Responsive**: Works seamlessly on all devices

## 📊 Project Overview

This application transforms raw Walmart sales data into actionable business intelligence through:

- **Data Analysis**: Historical sales patterns and trends
- **Feature Engineering**: Economic indicators, seasonal factors, and store characteristics
- **Model Training**: Ridge and Lasso regression algorithms
- **Web Interface**: User-friendly prediction forms and result visualization
- **API Access**: RESTful endpoints for integration

## 🛠 Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **scikit-learn 1.3.2**: Machine learning library
- **pandas 2.1.3**: Data manipulation
- **numpy 1.24.3**: Numerical computing
- **joblib 1.3.2**: Model serialization

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome 6**: Icon library
- **Chart.js**: Data visualization
- **Custom CSS**: Modern gradients and animations

### Database
- **SQLite**: Default development database
- **Configurable**: Support for PostgreSQL/MySQL

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Walmart+Sales+Forecasting
   ```

2. **Navigate to Django project**
   ```bash
   cd walmart_forecasting_app
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Web Interface: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Documentation: http://127.0.0.1:8000/api/predict/

## 🎯 Usage Guide

### Making Predictions

1. **Navigate to Home Page**: Open http://127.0.0.1:8000/
2. **Fill the Prediction Form**:
   - Store Number (1-45)
   - Department Number (1-99)
   - Holiday Week (checkbox)
   - Temperature (°F)
   - Consumer Price Index
   - Unemployment Rate (%)
   - Store Size (sq ft)
   - Week Number (1-52)
   - Year

3. **Click "Predict Sales"**: Get instant results with confidence scores

### Sample Data Testing

Click "Load Sample Data" to:
- Train ML models with sample dataset
- Test prediction functionality
- Explore features without real data

### Viewing History

Access "History" page to:
- View all past predictions
- Filter by store, year, or holiday status
- Export data to CSV
- Analyze prediction patterns

### API Usage

**Endpoint**: `POST /api/predict/`

**Parameters**:
```json
{
    "store": 1,
    "department": 1,
    "is_holiday": false,
    "temperature": 42.31,
    "cpi": 211.10,
    "unemployment": 8.1,
    "size": 151315,
    "week": 5,
    "year": 2010
}
```

**Response**:
```json
{
    "predicted_sales": 25000.00,
    "confidence_score": 0.85,
    "model_used": "ridge"
}
```

## 📈 Model Information

### Features Used
- **Store Characteristics**: Store number, size, type
- **Temporal Features**: Week number, year, holiday indicator
- **Economic Indicators**: CPI, unemployment rate, temperature
- **Department Information**: Department number

### Algorithms
- **Ridge Regression**: Primary prediction model
- **Lasso Regression**: Secondary model for confidence scoring
- **Feature Scaling**: StandardScaler for normalization

### Performance Metrics
- **Training R²**: ~0.084 (based on historical data)
- **Confidence Scoring**: Model agreement between Ridge and Lasso
- **Feature Importance**: Store size and holiday status are key predictors

## 🔧 Configuration

### Database Settings

**SQLite (Default)**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**PostgreSQL**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'walmart_forecasting',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Model Training

The application includes:
- **Sample Data Generator**: Creates realistic test data
- **Real Data Support**: Loads from CSV files if available
- **Automatic Training**: Initializes models on startup
- **Fallback Mechanisms**: Graceful error handling

## 🐛 Troubleshooting

### Common Issues

1. **Server Won't Start**
   - Check Python version (3.8+ required)
   - Verify virtual environment activation
   - Ensure all dependencies installed

2. **Prediction Errors**
   - Click "Load Sample Data" first
   - Check form validation messages
   - Verify input ranges

3. **Static Files Missing**
   - Run `python manage.py collectstatic`
   - Check STATICFILES_DIRS setting

4. **Database Issues**
   - Delete `db.sqlite3` and re-run migrations
   - Check file permissions

### Error Messages

- **"Models not trained yet"**: Click "Load Sample Data"
- **"Prediction error"**: Check input values and try again
- **"Form validation errors"**: Review highlighted fields

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with prediction form |
| POST | `/predict/` | Submit prediction request |
| GET | `/result/<id>/` | View specific prediction result |
| GET | `/history/` | View prediction history |
| POST | `/api/predict/` | API prediction endpoint |
| POST | `/sample-data/` | Load sample training data |

### Response Codes

- `200`: Success
- `400`: Bad Request (validation error)
- `404`: Not Found
- `405`: Method Not Allowed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational and demonstration purposes.

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the error messages
- Test with sample data first

## 🔄 Updates

### Version History
- **v1.0.0**: Initial release with ML prediction functionality
- **v1.1.0**: Added API endpoints and export features
- **v1.2.0**: Enhanced UI with responsive design

### Future Enhancements
- Additional ML algorithms (Random Forest, XGBoost)
- Real-time data integration
- Advanced analytics dashboard
- Mobile app companion
- Cloud deployment options

---

**Note**: This application demonstrates how to transform machine learning models into production-ready web applications. The sample data and models are for educational purposes.
