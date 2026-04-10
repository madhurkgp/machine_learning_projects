# COVID-19 Analysis Dashboard

A production-ready Django web application with machine learning capabilities for COVID-19 case prediction and analysis.

## Features

- **Real-time Predictions**: ML-powered predictions for COVID-19 cases using Random Forest models
- **Interactive Dashboard**: Modern, responsive interface with real-time statistics
- **Data Visualization**: Interactive charts and graphs using Chart.js
- **Prediction History**: Track and analyze past predictions with confidence scores
- **Admin Panel**: Comprehensive Django admin interface for data management
- **API Endpoints**: RESTful API for programmatic access
- **Export Functionality**: Export data as JSON or CSV
- **Mobile Responsive**: Fully responsive design for all devices

## Technology Stack

- **Backend**: Django 4.2.7
- **Machine Learning**: scikit-learn 1.3.2 (Random Forest)
- **Data Processing**: pandas 2.1.3, numpy 1.24.3
- **Frontend**: Bootstrap 5, Chart.js, Custom CSS
- **Database**: SQLite (development ready)
- **Deployment**: Gunicorn, WhiteNoise

## Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   cd "d:\project_learning\Machine_Learning\Covid-19+Analysis+Files"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```
   - Username: `admin`
   - Password: `admin123`

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Dashboard: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API: http://127.0.0.1:8000/api/predict/

## Usage Guide

### Making Predictions

1. Navigate to the **Predict** page from the main menu
2. Enter current COVID-19 data for your region:
   - State name
   - Current cases (active, positive, cured, deaths)
   - New cases (today's numbers)
3. Click **Get Predictions** to receive ML-powered forecasts
4. View results with confidence scores and trend analysis

### Loading Sample Data

1. From the dashboard, click **Load Sample Data**
2. This will populate the system with sample COVID-19 data
3. Use this data to test predictions and visualizations

### Viewing Visualizations

1. Navigate to **Visualization** in the menu
2. Choose from different chart types:
   - Line charts for trends
   - Bar charts for comparisons
   - Pie charts for distributions
3. Filter by date range and data type

### API Usage

#### Make a Prediction via API

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "state_name": "Maharashtra",
    "active_cases": 55351,
    "positive_cases": 1969114,
    "cured_cases": 1863702,
    "death_cases": 50061,
    "new_active": 53463,
    "new_positive": 1971552,
    "new_cured": 1867988,
    "new_death": 50101
  }'
```

#### Response Format

```json
{
    "status": "success",
    "prediction_id": 123,
    "results": {
        "predicted_active": 56000,
        "predicted_positive": 1970000,
        "predicted_cured": 1870000,
        "predicted_death": 50200,
        "confidence_score": 0.85
    }
}
```

## Model Information

### Machine Learning Model

- **Algorithm**: Random Forest Regressor
- **Features**: 8 input variables (current and new cases)
- **Targets**: 4 prediction outputs (future case numbers)
- **Training**: Automatically trained on sample data
- **Confidence**: 75-95% confidence scores for predictions

### Input Features

1. Active Cases
2. Positive Cases
3. Cured Cases
4. Death Cases
5. New Active Cases
6. New Positive Cases
7. New Cured Cases
8. New Death Cases

### Prediction Targets

1. Predicted Active Cases
2. Predicted Positive Cases
3. Predicted Cured Cases
4. Predicted Death Cases

## Project Structure

```
Covid-19+Analysis+Files/
|-- covid_analysis/          # Django project settings
|-- prediction/              # Main Django app
|   |-- models.py           # Database models
|   |-- views.py            # View functions
|   |-- urls.py             # URL routing
|   |-- admin.py            # Admin configuration
|   |-- ml_model.py         # Machine learning model
|   |-- migrations/         # Database migrations
|-- templates/               # HTML templates
|   |-- base.html
|   |-- prediction/         # App-specific templates
|-- static/                  # Static files
|   |-- css/style.css      # Custom styles
|   |-- js/main.js         # JavaScript utilities
|-- requirements.txt         # Python dependencies
|-- README.md               # This file
|-- manage.py              # Django management script
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Settings

- **Development**: SQLite (default)
- **Production**: PostgreSQL recommended

### Static Files

- **Development**: Served by Django
- **Production**: Use WhiteNoise or CDN

## Deployment

### Production Setup

1. **Install production dependencies**
   ```bash
   pip install gunicorn whitenoise
   ```

2. **Set environment variables**
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=yourdomain.com
   ```

3. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

4. **Run with Gunicorn**
   ```bash
   gunicorn covid_analysis.wsgi:application
   ```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "covid_analysis.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Ensure all dependencies are installed
   - Check that model files exist in `prediction/` directory

2. **Database Migration Issues**
   ```bash
   python manage.py migrate --fake-initial
   ```

3. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Permission Errors**
   - Ensure proper file permissions for model files
   - Check database file permissions

### Error Messages

- **"No pre-trained model found"**: The system will automatically train a new model
- **"Validation errors"**: Check that all input values are non-negative numbers
- **"Database error"**: Run migrations and check database connection

## Contributing

### Development Guidelines

1. Follow PEP 8 for Python code
2. Use meaningful variable names
3. Add comments for complex logic
4. Test all new features
5. Update documentation

### Adding New Features

1. Create feature branch
2. Add models, views, templates
3. Update URLs and admin
4. Add tests
5. Update documentation

## API Documentation

### Endpoints

- `GET /` - Dashboard
- `GET /predict/` - Prediction form
- `POST /api/predict/` - Make prediction
- `GET /visualization/` - Data charts
- `GET /history/` - Prediction history
- `GET /model-info/` - Model details

### Response Codes

- `200` - Success
- `400` - Bad Request (validation error)
- `500` - Server Error

## License

This project is for educational and research purposes. Please ensure compliance with local regulations when using COVID-19 data.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the error logs
3. Verify all dependencies are installed
4. Test with sample data first

## Version History

- **v1.0.0** - Initial release with ML predictions and dashboard
- Features: Random Forest model, responsive UI, API endpoints, admin panel

---

**Built with Django, scikit-learn, and modern web technologies**
