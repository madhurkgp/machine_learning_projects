# Indian Air Quality Prediction System

A production-ready Django web application that predicts Air Quality Index (AQI) based on pollutant concentrations using machine learning models.

## Features

- **Real-time AQI Prediction**: Calculate Air Quality Index from SO2, NO2, RSPM, and SPM concentrations
- **Modern UI/UX**: Responsive, gradient-based design with smooth animations
- **ML Integration**: Uses trained Random Forest models with 99.9% accuracy
- **Sample Data**: Built-in sample data for easy testing
- **Prediction History**: View recent predictions with timestamps
- **API Endpoint**: RESTful API for programmatic access
- **Admin Panel**: Django admin for managing prediction data

## Technology Stack

- **Backend**: Django 4.2.7
- **Machine Learning**: scikit-learn 1.3.2
- **Data Processing**: pandas 2.1.3, numpy 1.24.3
- **Model Serialization**: joblib 1.3.2
- **Frontend**: Modern CSS3 with gradients and animations
- **Database**: SQLite (development ready)

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup Instructions

1. **Clone or navigate to the project directory:**
   ```bash
   cd "d:\project_learning\Machine_Learning\Indian+Air+Quality+prediction"
   ```

2. **Create and activate virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train and save ML models:**
   ```bash
   python train_models.py
   ```
   This will:
   - Process the air quality dataset
   - Train Random Forest regression and classification models
   - Save models to the `models/` directory
   - Display model accuracy scores

5. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000`

## Usage

### Web Interface

1. **Fill the prediction form** with pollutant concentrations:
   - **SO2**: Sulphur Dioxide concentration (µg/m³)
   - **NO2**: Nitrogen Dioxide concentration (µg/m³)
   - **RSPM**: Respirable Suspended Particulate Matter (µg/m³)
   - **SPM**: Suspended Particulate Matter (µg/m³)

2. **Click "Predict Air Quality"** to get:
   - AQI value (0-500+ scale)
   - AQI category (Good, Moderate, Poor, Unhealthy, Very unhealthy, Hazardous)
   - Individual pollutant indices
   - Color-coded health impact visualization

3. **Use "Sample Data"** button to test with pre-filled values

### API Endpoint

Send POST requests to `/api/predict/` with the following parameters:

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -d "so2=15.2&no2=25.8&rspm=45.3&spm=78.5"
```

**Response format:**
```json
{
  "success": true,
  "aqi_value": 67.8,
  "aqi_category": "Moderate",
  "aqi_color": "#ffff00",
  "pollutant_indices": {
    "SOi": 19.0,
    "Noi": 32.25,
    "Rpi": 75.5,
    "SPMi": 78.5
  }
}
```

## Model Information

### Dataset
- **Source**: Historical Daily Ambient Air Quality Data (1990-2015)
- **Provider**: Ministry of Environment and Forests, Government of India
- **Size**: 435,742 records across 37 Indian states

### Features
- **SOi**: Sulphur Dioxide individual pollutant index
- **Noi**: Nitrogen Dioxide individual pollutant index  
- **Rpi**: Respirable Suspended Particulate Matter index
- **SPMi**: Suspended Particulate Matter index

### Models
- **Regression Model**: Random Forest Regressor (R²: 0.9994)
- **Classification Model**: Random Forest Classifier (Accuracy: 99.93%)

### AQI Categories
| Range | Category | Color | Health Impact |
|-------|----------|-------|---------------|
| 0-50 | Good | Green | Air quality satisfactory |
| 51-100 | Moderate | Yellow | Acceptable for most |
| 101-200 | Poor | Orange | Sensitive groups affected |
| 201-300 | Unhealthy | Red | Everyone affected |
| 301-400 | Very Unhealthy | Purple | Health warnings |
| 401+ | Hazardous | Maroon | Emergency conditions |

## Project Structure

```
Indian+Air+Quality+prediction/
|
|-- airquality_project/          # Django project settings
|   |-- settings.py              # Project configuration
|   |-- urls.py                 # Main URL routing
|   |-- wsgi.py                 # WSGI configuration
|
|-- prediction/                 # Django app
|   |-- models.py               # Database models
|   |-- views.py                # Business logic & ML integration
|   |-- forms.py                # Form definitions
|   |-- urls.py                 # App URL routing
|   |-- admin.py                # Admin interface
|   |-- templates/prediction/   # HTML templates
|   |-- migrations/             # Database migrations
|
|-- models/                     # Trained ML models
|   |-- rf_regression_model.pkl
|   |-- rf_classification_model.pkl
|   |-- feature_names.pkl
|
|-- static/                     # Static files
|   |-- css/style.css           # Modern CSS styling
|   |-- js/                     # JavaScript files
|
|-- Note Book/                  # Original analysis
|   |-- 7.Indian Air Quality.ipynb
|   |-- data.csv                # Training dataset
|   |-- Descriptionfile.txt
|
|-- train_models.py             # Model training script
|-- requirements.txt            # Python dependencies
|-- manage.py                   # Django management script
|-- README.md                   # This file
```

## Development

### Adding New Features

1. **New Models**: Add to `train_models.py` and update `views.py`
2. **UI Changes**: Modify templates in `prediction/templates/`
3. **API Endpoints**: Add to `prediction/urls.py` and `prediction/views.py`
4. **Database Changes**: Create migrations with `python manage.py makemigrations`

### Testing

```bash
# Run Django tests
python manage.py test

# Test specific app
python manage.py test prediction

# Test with coverage (if installed)
coverage run --source='.' manage.py test
coverage report
```

### Production Deployment

1. **Set environment variables:**
   ```bash
   export DEBUG=False
   export SECRET_KEY='your-production-secret-key'
   export ALLOWED_HOSTS='yourdomain.com'
   ```

2. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

3. **Use production web server:**
   ```bash
   gunicorn airquality_project.wsgi:application
   ```

## Troubleshooting

### Common Issues

1. **Model Loading Error**:
   - Ensure `train_models.py` was run successfully
   - Check that `models/` directory contains `.pkl` files

2. **Database Migration Error**:
   - Delete `db.sqlite3` and re-run migrations
   - Clear migrations folder and regenerate

3. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATIC_ROOT` settings

4. **Server Not Starting**:
   - Check if port 8000 is in use
   - Try different port: `python manage.py runserver 8080`

### Performance Optimization

1. **Model Caching**: Models are loaded once per request
2. **Database Indexing**: Add indexes on frequently queried fields
3. **Static File Compression**: Use CDN for production
4. **Async Processing**: Consider Celery for long-running predictions

## API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main prediction interface |
| POST | `/` | Submit prediction form |
| GET | `/sample-data/` | Load sample data |
| POST | `/api/predict/` | API prediction endpoint |

### Error Responses

```json
{
  "success": false,
  "error": "Error message description"
}
```

## Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## License

This project is for educational and research purposes. The dataset is provided by the Government of India under the National Data Sharing and Accessibility Policy (NDSAP).

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Django documentation
3. Create an issue with detailed description

## Acknowledgments

- Ministry of Environment and Forests, Government of India
- Central Pollution Control Board of India
- scikit-learn development team
- Django framework contributors
