# Black Friday Sale Prediction

A production-ready Django web application that predicts customer purchase amounts during Black Friday sales using machine learning.

## 🚀 Features

- **Machine Learning Prediction**: Uses a Random Forest Regressor trained on 550,000+ customer transactions
- **Modern UI**: Responsive, mobile-friendly interface with Bootstrap 5 and custom CSS
- **Real-time Validation**: Form validation with helpful error messages
- **Sample Data**: One-click sample data for easy testing
- **Feature Importance**: Visual display of key predictive factors
- **API Endpoints**: RESTful API for programmatic access
- **Professional Design**: Clean, modern interface with gradients and animations

## 📊 Model Performance

- **Model Type**: Random Forest Regressor
- **Training Samples**: 550,068 customer transactions
- **R² Score**: 0.77 (77% variance explained)
- **RMSE**: 0.35 (log scale)
- **Features**: 12 predictive features including demographics and product categories

## 🛠️ Technology Stack

### Backend
- **Django 4.2**: Web framework
- **Python 3.10**: Programming language
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **joblib**: Model serialization

### Frontend
- **Bootstrap 5**: CSS framework
- **Font Awesome**: Icons
- **JavaScript**: Interactive features
- **CSS3**: Custom styling and animations

### ML Pipeline
- **Random Forest**: Ensemble learning algorithm
- **StandardScaler**: Feature normalization
- **LabelEncoder**: Categorical variable encoding
- **Feature Engineering**: Data preprocessing pipeline

## 📁 Project Structure

```
black friday sale prediction/
├── blackfriday/                 # Django project settings
│   ├── settings.py             # Project configuration
│   ├── urls.py                 # Root URL patterns
│   └── wsgi.py                 # WSGI configuration
├── prediction/                 # Django app
│   ├── views.py                # View functions
│   ├── forms.py                # Django forms
│   ├── ml_utils.py             # ML prediction utilities
│   ├── urls.py                 # App URL patterns
│   └── templatetags/           # Custom template filters
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   └── prediction/             # App templates
├── static/                     # Static files
│   ├── css/style.css           # Custom styles
│   └── js/main.js              # JavaScript
├── models/                     # Trained ML models
│   ├── random_forest_model.pkl # Trained model
│   ├── feature_scaler.pkl      # Feature scaler
│   └── preprocessing_info.pkl # Preprocessing data
├── Notebook/                   # Original ML analysis
│   ├── Black Friday.ipynb      # Jupyter notebook
│   ├── train.csv               # Training data
│   └── test.csv                # Test data
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── train_model.py              # Model training script
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager
- Git (optional)

### Installation

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd "black friday sale prediction"
   ```

2. **Create and activate virtual environment**
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

4. **Train the ML model**
   ```bash
   python train_model.py
   ```
   This will:
   - Load and preprocess the training data
   - Train a Random Forest model
   - Save the model and preprocessing objects to the `models/` directory

5. **Run Django migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## 📖 Usage Guide

### Making Predictions

1. **Fill the Form**: Enter customer information including:
   - User ID and Product ID
   - Demographics (Gender, Age, Occupation)
   - Location (City Category, Years in City)
   - Product Categories

2. **Use Sample Data**: Click "Fill Sample Data" to auto-populate the form with test values

3. **Get Prediction**: Click "Predict Purchase" to see the predicted amount

4. **View Results**: The prediction displays with:
   - Predicted purchase amount in USD
   - Feature importance analysis
   - Confidence indicators

### API Usage

The application provides RESTful API endpoints:

#### Predict Purchase Amount
```bash
POST /api/predict/
Content-Type: application/json

{
    "user_id": 1000001,
    "product_id": "P00069042",
    "gender": "M",
    "age": "26-35",
    "occupation": 10,
    "city_category": "A",
    "stay_years": "2",
    "marital_status": 0,
    "product_category_1": 3,
    "product_category_2": 6.0
}
```

**Response:**
```json
{
    "success": true,
    "prediction": 8370,
    "formatted_prediction": "$8,370"
}
```

#### Get Sample Data
```bash
GET /sample-data/
```

### Model Features

The prediction model uses the following features:

**Demographic Features:**
- User ID: Unique customer identifier
- Gender: Male/Female
- Age: Age groups (0-17, 18-25, 26-35, 36-45, 46-50, 51-55, 55+)
- Occupation: Occupation codes (0-20)
- Marital Status: Single (0) or Married (1)

**Location Features:**
- City Category: Urban (A), Suburban (B), Rural (C)
- Stay Years: Years in current city (0, 1, 2, 3, 4+)

**Product Features:**
- Product ID: Unique product identifier
- Product Category 1: Primary product category (1-20)
- Product Category 2: Secondary product category (2-18)

## 🔧 Configuration

### Django Settings

Key settings in `blackfriday/settings.py`:

```python
DEBUG = True  # Set to False for production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Add your domain for production
SECRET_KEY = 'your-secret-key-here'  # Change for production
```

### Model Parameters

Model configuration in `train_model.py`:

```python
model = RandomForestRegressor(
    n_estimators=50,      # Number of trees
    random_state=42,      # Reproducibility
    max_depth=15         # Tree depth for memory efficiency
)
```

## 🧪 Testing

### Manual Testing

1. **Basic Functionality**:
   - Navigate to the home page
   - Fill out the prediction form
   - Verify prediction results

2. **Form Validation**:
   - Test with invalid inputs
   - Verify error messages
   - Test edge cases

3. **Sample Data**:
   - Click "Fill Sample Data"
   - Verify form population
   - Test prediction with sample data

### Automated Testing

Run Django tests:
```bash
python manage.py test
```

### API Testing

Test API endpoints:
```bash
# Test prediction endpoint
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1000001, "product_id": "P00069042", ...}'
```

## 🚀 Deployment

### Production Setup

1. **Environment Variables**:
   ```bash
   export DEBUG=False
   export SECRET_KEY='your-production-secret-key'
   export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
   ```

2. **Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Database**:
   - Configure production database in settings
   - Run migrations: `python manage.py migrate`

4. **Web Server**:
   - Use Gunicorn for production:
   ```bash
   pip install gunicorn
   gunicorn blackfriday.wsgi:application
   ```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python train_model.py
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "blackfriday.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Error**:
   - Ensure `train_model.py` has been run
   - Check that `models/` directory exists and contains all files
   - Verify file permissions

2. **Memory Issues**:
   - The model uses ~50MB RAM
   - Reduce `n_estimators` in `train_model.py` if needed
   - Close other applications to free memory

3. **Django Server Issues**:
   - Check for port conflicts (default: 8000)
   - Verify virtual environment is activated
   - Ensure all dependencies are installed

4. **Form Validation Errors**:
   - Check field constraints in `forms.py`
   - Verify data types match expected formats
   - Review error messages for specific issues

### Debug Mode

Enable debug logging in `blackfriday/settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

## 📈 Performance Optimization

### Model Optimization

- **Feature Selection**: The model uses 12 optimized features
- **Memory Efficiency**: Reduced to 50 trees for lower memory usage
- **Prediction Speed**: Average prediction time < 100ms

### Web Performance

- **Static Files**: CSS and JS are minified and cached
- **Database**: Uses SQLite for development (switch to PostgreSQL for production)
- **Caching**: Add Redis caching for production deployments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -m "Add feature description"`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Review the troubleshooting section
- Check the model documentation in `Notebook/Black Friday.ipynb`

## 🔄 Version History

- **v1.0.0**: Initial production release
  - Django web application
  - ML model integration
  - Responsive UI
  - API endpoints
  - Complete documentation

---

**Built with ❤️ using Django and Machine Learning**
