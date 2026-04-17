# Sonic Log Predictor

Advanced Machine Learning system for predicting DTC (Compressional Travel-time) and DTS (Shear Travel-time) values from well log data using XGBoost with Wavelet Transformation.

## 🚀 Features

- **High Accuracy**: R² scores of 0.982 for DTC and 0.999 for DTS predictions
- **Wavelet Transformation**: Advanced signal processing for enhanced feature extraction
- **Modern UI**: Responsive Bootstrap 5 interface with real-time validation
- **REST API**: Programmatic access to prediction capabilities
- **Sample Data**: Built-in sample data for easy testing
- **History Tracking**: Complete prediction history with detailed analysis
- **Export Functionality**: Export predictions in JSON format

## 📊 Model Performance

| Metric | DTC Prediction | DTS Prediction |
|--------|----------------|----------------|
| R² Score | 0.982 | 0.999 |
| RMSE | 3.17 ns/ft | 2.34 ns/ft |
| Algorithm | XGBoost + Wavelet | XGBoost + Wavelet |

## 🛠️ Technology Stack

### Machine Learning
- **XGBoost**: Gradient boosting framework
- **PyWavelets**: Wavelet transformation library
- **scikit-learn**: Machine learning utilities
- **pandas**: Data manipulation
- **numpy**: Numerical computing

### Web Development
- **Django 4.2.7**: Web framework
- **Bootstrap 5**: Responsive UI framework
- **Chart.js**: Data visualization
- **SQLite**: Database (configurable)

## 📋 Input Features

| Feature | Description | Unit | Range |
|---------|-------------|------|-------|
| CAL | Caliper | Inch | 6-12 |
| CNC | Neutron Log | decimal | 0-0.7 |
| GR | Gamma Ray | API | 0-250 |
| HRD | Deep Resistivity | Ohm/m | Variable |
| HRM | Medium Resistivity | Ohm/m | Variable |
| PE | Photo-electric Factor | Barn | 1-10 |
| ZDEN | Density | g/m³ | 2-3 |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd "Sonic+log+Code+and+Files"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000`

## 📖 Usage Guide

### Making Predictions

1. **Navigate to Home Page**: The main page provides the prediction form
2. **Input Well Log Data**: Fill in the 7 input parameters
3. **Use Sample Data**: Click "Load Sample" to test with pre-filled values
4. **Submit Prediction**: Click "Make Prediction" to get results
5. **View Results**: See DTC and DTS predictions with analysis

### Using Sample Data

The application provides three sample datasets:
- **Sample 1**: High density formation
- **Sample 2**: Medium density formation  
- **Sample 3**: Low density formation

Click "Load Sample" to randomly populate the form with realistic data.

### Viewing History

1. Click "View History" in the navigation
2. Browse all previous predictions
3. Click "View Details" for in-depth analysis
4. Export data using the "Export" button

### API Access

Send POST requests to `/api/predict/` with the following parameters:

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -d "cal=8.5781&cnc=0.3521&gr=55.1824&hrd=0.8121&hrm=0.7810&pe=6.8291&zden=2.3256"
```

Response format:
```json
{
  "success": true,
  "dtc": 107.52,
  "dts": 212.88,
  "method": "xgboost_wavelet"
}
```

## 🧠 Model Details

### Data Preprocessing

1. **Missing Value Handling**: Replace -999 with NaN and fill with mean
2. **Outlier Removal**: Apply domain-specific thresholds
3. **Log Transformation**: Apply log to resistivity values
4. **Wavelet Features**: Generate db4 wavelet coefficients from CNC log

### Feature Engineering

- **Wavelet Transformation**: Applied to CNC (Neutron Log) using db4 wavelet
- **Multi-level Decomposition**: Levels 1-4 for both approximate and detailed coefficients
- **Interpolation**: Maintain original data length after transformation

### Model Architecture

- **Base Algorithm**: XGBoost Regressor
- **Hyperparameters**: Optimized for each target variable
- **Training Data**: 20,036 samples from synthetic well logs
- **Validation**: 30% holdout test set

## 📁 Project Structure

```
Sonic+log+Code+and+Files/
├── Code and Files/                 # Original ML notebook and data
│   ├── Wavelet Transformation project.ipynb
│   ├── train.csv
│   ├── test.csv
│   └── real_test_result.csv
├── prediction/                     # Django app
│   ├── models.py                   # Database models
│   ├── views.py                    # Application logic
│   ├── forms.py                    # Form definitions
│   ├── ml_models.py                # ML prediction logic
│   ├── urls.py                     # URL routing
│   ├── admin.py                    # Admin interface
│   └── templates/prediction/       # HTML templates
├── sonic_log_predictor/            # Django project
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # Main URL routing
│   └── wsgi.py                    # WSGI configuration
├── static/                         # Static files
├── manage.py                       # Django management script
├── requirements.txt                 # Python dependencies
└── README.md                       # This file
```

## 🔧 Configuration

### Database Settings

Default: SQLite (`db.sqlite3`)

To use PostgreSQL or MySQL, modify `sonic_log_predictor/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sonic_log_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Production Settings

For production deployment:

1. **Set DEBUG=False** in settings
2. **Configure ALLOWED_HOSTS** with your domain
3. **Set STATIC_ROOT** for static files
4. **Use environment variables** for sensitive settings

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install missing dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. **Static files not loading**: Run collectstatic
   ```bash
   python manage.py collectstatic
   ```

3. **Database errors**: Run migrations
   ```bash
   python manage.py migrate
   ```

4. **Port already in use**: Use different port
   ```bash
   python manage.py runserver 8080
   ```

### Performance Tips

- Use SSD for database storage
- Enable Django caching for production
- Consider Redis for session storage
- Use Gunicorn for production deployment

## 📈 Performance Benchmarks

| Operation | Average Time |
|-----------|--------------|
| Single Prediction | < 1 second |
| Data Preprocessing | < 0.5 seconds |
| Wavelet Transformation | < 0.3 seconds |
| Database Query | < 0.1 seconds |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or issues:
- Check the troubleshooting section
- Review the model documentation
- Create an issue in the repository

## 🎯 Future Enhancements

- [ ] Real-time streaming predictions
- [ ] Advanced visualization dashboard
- [ ] Model versioning and A/B testing
- [ ] Integration with well logging software
- [ ] Mobile application
- [ ] Cloud deployment options

---

**Built with ❤️ using Django and Advanced Machine Learning**
