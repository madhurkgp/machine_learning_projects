# Pore Pressure Prediction System

A production-ready Django web application that uses Machine Learning to predict pore pressure in oil and gas exploration wells.

## 🚀 Features

- **ML-Powered Predictions**: Random Forest model with 95.13% R² accuracy
- **Modern Web Interface**: Responsive Bootstrap 5 design with real-time validation
- **REST API**: Programmatic access for integration with other systems
- **Data History**: Track and export prediction history
- **Sample Data**: One-click sample data for easy testing
- **Professional UI**: Clean, modern interface with gradients and animations

## 📊 Model Performance

- **Algorithm**: Random Forest Regressor
- **Accuracy**: 95.13% R² score
- **Training Data**: 8 wells, 10,408 samples
- **Features**: 9 input parameters
- **MAE**: 25.24 PSI
- **RMSE**: 45.64 PSI

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **ML Framework**: scikit-learn 1.3.2
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite (configurable)
- **Data Processing**: pandas, numpy

## 📋 Input Parameters

| Parameter | Description | Range | Units |
|-----------|-------------|-------|-------|
| Depth | Distance from surface | 0-10000 | meters |
| GR | Gamma Ray reading | 70-150 | API units |
| RHOB | Bulk density | 1.5-3.0 | g/cm³ |
| Vp | P-wave velocity | 1.0-1.7 | km/s |
| Vsh | Shale volume | 0.37-1.0 | fraction |
| Caliper | Well bore diameter | < 11 | inches |
| Porosity | Rock porosity | < 75 | percent |
| Resistivity | Formation resistivity | < 1.5 | ohm-m |
| Stress | Overburden stress | 0-10M | Pa |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd "Pore pressure Code and Files"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix
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

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open in browser**
   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📖 Usage

### Web Interface

1. **Fill Input Form**: Enter the 9 required parameters
2. **Use Sample Data**: Click "Fill Sample Data" for quick testing
3. **Get Prediction**: Click "Predict Pore Pressure" to see results
4. **View History**: Recent predictions appear in the history table

### API Usage

#### Make Prediction

**Endpoint**: `POST /api/predict/`

**Headers**:
```
Content-Type: application/json
X-CSRFToken: [csrf_token]  # Required for web requests
```

**Request Body**:
```json
{
    "depth": 100.0,
    "gr": 85.5,
    "rhob": 2.1,
    "vp": 1.5,
    "vsh": 0.65,
    "caliper": 8.5,
    "porosity": 45.0,
    "resistivity": 0.9,
    "stress": 1500000.0
}
```

**Response**:
```json
{
    "success": true,
    "predicted_pp": 1750.25,
    "confidence_score": 0.85,
    "prediction_id": 123
}
```

#### Get Sample Data

**Endpoint**: `GET /api/sample/`

**Response**: Returns sample data for testing

## 🏗️ Project Structure

```
pore_pressure_app/
├── pore_pressure_app/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── prediction/                 # Main Django app
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── forms.py               # Django forms
│   ├── ml_model.py            # ML model integration
│   ├── urls.py                # App URLs
│   └── templates/prediction/  # HTML templates
├── static/                    # CSS, JavaScript, images
│   ├── css/style.css
│   └── js/main.js
├── models/                    # Trained ML models (auto-generated)
├── requirements.txt           # Python dependencies
├── manage.py                 # Django management script
└── well *.csv                # Training data files
```

## 🔧 Configuration

### Database Settings

Default: SQLite (`db.sqlite3`)

To use PostgreSQL or MySQL, update `pore_pressure_app/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pore_pressure_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Model Retraining

The system automatically trains the model on first run. To retrain:

```python
from prediction.ml_model import predictor
predictor.train_model()
```

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Manual Testing

1. **Web Interface Test**:
   - Navigate to home page
   - Click "Fill Sample Data"
   - Submit form
   - Verify prediction appears

2. **API Test**:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/predict/ \
   -H "Content-Type: application/json" \
   -d '{"depth":100.0,"gr":85.5,"rhob":2.1,"vp":1.5,"vsh":0.65,"caliper":8.5,"porosity":45.0,"resistivity":0.9,"stress":1500000.0}'
   ```

## 📈 Model Details

### Data Preprocessing

1. **Outlier Removal**: Values outside recommended ranges are filtered
2. **Feature Scaling**: MinMax scaling applied to all features
3. **Data Quality**: Missing values handled appropriately

### Feature Importance

The Random Forest model automatically determines feature importance during training. Key features typically include:
- Stress (most important)
- Depth
- Resistivity
- Porosity
- RHOB

### Confidence Scoring

Confidence scores are calculated based on:
- Input parameter ranges
- Feature distribution in training data
- Model uncertainty estimation

**Score Interpretation**:
- 0.8-1.0: High confidence
- 0.6-0.8: Medium confidence
- <0.6: Low confidence

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Error**:
   - Ensure all CSV files are present
   - Check file permissions
   - Verify Python dependencies

2. **Database Migration Error**:
   ```bash
   python manage.py makemigrations prediction
   python manage.py migrate
   ```

3. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATICFILES_DIRS` settings

4. **API CSRF Error**:
   - Include CSRF token in requests
   - For external APIs, consider using CSRF exempt decorator

### Performance Optimization

1. **Database**: Add indexes to frequently queried fields
2. **Model**: Cache predictions for repeated inputs
3. **Frontend**: Implement pagination for history table

## 📝 License

This project is for educational and research purposes. Please cite appropriately if used in academic work.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the API documentation
- Open an issue with detailed error information

---

**Note**: This system is designed for educational purposes. For production use in critical oil and gas operations, additional validation and testing are recommended.
