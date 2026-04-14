# Zomato Restaurant Rating Predictor

A production-ready Django web application that predicts restaurant ratings using Machine Learning algorithms. This application transforms raw ML models into an interactive, user-friendly platform for restaurant rating analysis.

## Features

### Core Functionality
- **ML-Powered Predictions**: Uses Random Forest, Linear Regression, and Decision Tree models
- **Real-time Analysis**: Instant restaurant rating predictions with confidence scores
- **Interactive Dashboard**: Comprehensive analytics and visualization
- **Responsive Design**: Modern UI that works on all devices
- **Sample Data**: Built-in sample data for easy testing

### ML Models
- **Random Forest Regressor**: 87.5% accuracy (R² score)
- **Linear Regression**: Baseline model for comparison
- **Decision Tree Regressor**: 79.4% accuracy
- **Fallback Rule-based**: Ensures predictions even when models fail

### User Interface
- **Modern Design**: Clean, professional interface with Bootstrap 5
- **Form Validation**: Client and server-side validation
- **Visual Feedback**: Loading states, animations, and progress indicators
- **Analytics Dashboard**: Charts and insights using Chart.js

## Tech Stack

### Backend
- **Django 4.2.7**: Web framework
- **scikit-learn 1.3.2**: Machine learning
- **pandas 2.1.4**: Data manipulation
- **numpy 1.25.2**: Numerical computing
- **joblib 1.3.2**: Model serialization

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **Chart.js**: Data visualization
- **Font Awesome**: Icons
- **Custom CSS/JS**: Enhanced user experience

### Database
- **SQLite**: Development database (easily configurable for PostgreSQL/MySQL)

## Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Zomato+Restaurant+Analysis
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

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000`

## Usage Guide

### Making a Prediction

1. **Navigate to Home**: Click "Predict Rating" on the homepage
2. **Fill the Form**: 
   - Select online order availability
   - Choose table booking option
   - Enter number of votes
   - Select location, restaurant type, and cuisine
   - Enter approximate cost for two people
3. **Get Prediction**: Click "Predict Rating" to see results
4. **View Results**: See predicted rating, model used, and confidence score

### Using Sample Data

Click the "Load Sample Data" button to automatically fill the form with example values for testing.

### Viewing Analytics

1. **History Page**: View all past predictions with filtering options
2. **Analytics Dashboard**: Comprehensive insights and visualizations
3. **Model Performance**: Compare different ML models

### API Usage

The application provides a REST API endpoint for programmatic access:

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "online_order": true,
    "book_table": false,
    "votes": 150,
    "location": "BTM",
    "rest_type": "Quick Bites",
    "cuisines": "North Indian, Chinese",
    "approx_cost": 300
  }'
```

## Project Structure

```
Zomato+Restaurant+Analysis/
|-- manage.py                     # Django management script
|-- zomato_analysis/              # Main Django project
|   |-- __init__.py
|   |-- settings.py               # Django settings
|   |-- urls.py                   # Main URL configuration
|   |-- wsgi.py                   # WSGI configuration
|   |-- asgi.py                   # ASGI configuration
|-- restaurant/                   # Main Django app
|   |-- __init__.py
|   |-- admin.py                  # Django admin configuration
|   |-- apps.py                   # App configuration
|   |-- forms.py                  # Form classes
|   |-- models.py                 # Database models
|   |-- views.py                  # View functions
|   |-- urls.py                   # App URL configuration
|   |-- ml_models.py              # ML model integration
|   |-- migrations/                # Database migrations
|   |-- saved_models/             # Trained model files
|-- templates/                    # HTML templates
|   |-- base.html                 # Base template
|   |-- restaurant/               # App-specific templates
|       |-- home.html
|       |-- result.html
|       |-- history.html
|       |-- analytics.html
|-- static/                        # Static files
|   |-- css/
|   |   |-- style.css
|   |-- js/
|   |   |-- script.js
|-- media/                        # User uploads
|-- requirements.txt              # Python dependencies
|-- README.md                     # This file
```

## ML Model Details

### Feature Engineering
- **Categorical Encoding**: Label encoding for location, restaurant type, and cuisine
- **Boolean Features**: Online order and table booking availability
- **Numerical Features**: Votes and approximate cost
- **Target Variable**: Restaurant rating (1.0 - 5.0)

### Model Training
- **Data Source**: Zomato Bangalore restaurants dataset
- **Preprocessing**: Data cleaning, missing value handling, feature encoding
- **Validation**: Train-test split with performance metrics
- **Persistence**: Models saved using joblib for quick loading

### Performance Metrics
- **Random Forest**: R² = 0.875, MSE = 0.124
- **Linear Regression**: R² = 0.349, MSE = 0.652
- **Decision Tree**: R² = 0.794, MSE = 0.206

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Settings
For production, update `zomato_analysis/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'zomato_analysis',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with prediction form |
| POST | `/` | Submit prediction form |
| GET | `/result/<id>/` | View prediction result |
| GET | `/history/` | View prediction history |
| GET | `/analytics/` | Analytics dashboard |
| POST | `/api/predict/` | REST API for predictions |
| GET | `/load-sample/` | Load sample data |

## Testing

### Running Tests
```bash
python manage.py test
```

### Manual Testing Checklist
- [ ] Form validation works correctly
- [ ] Predictions are generated successfully
- [ ] Confidence scores are displayed
- [ ] Analytics dashboard loads with charts
- [ ] Responsive design works on mobile
- [ ] API endpoint returns valid JSON
- [ ] Error handling works properly

## Deployment

### Production Setup

1. **Set environment variables**
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-production-secret-key
   export ALLOWED_HOSTS=yourdomain.com
   ```

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Run with production server**
   ```bash
   gunicorn zomato_analysis.wsgi:application
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
CMD ["gunicorn", "zomato_analysis.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Check if `saved_models/` directory exists
   - Verify model files are not corrupted
   - Fallback to rule-based predictions

2. **Database Migration Issues**
   ```bash
   python manage.py migrate --fake-initial
   ```

3. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic --clear
   ```

4. **Import Errors**
   - Verify all dependencies are installed
   - Check Python version compatibility

### Performance Optimization

1. **Enable Caching**
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
       }
   }
   ```

2. **Database Indexing**
   - Add indexes to frequently queried fields
   - Use `select_related` and `prefetch_related`

3. **Static File Optimization**
   - Use CDN for static files
   - Enable gzip compression

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Zomato**: For providing the restaurant dataset
- **scikit-learn**: For excellent ML algorithms
- **Django**: For the robust web framework
- **Bootstrap**: For the responsive UI components

## Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting guide
- Review the API documentation

---

**Built with Django, scikit-learn, and modern web technologies**
