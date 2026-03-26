# Medical Cost Prediction - AI Powered Insurance Cost Estimator

A production-ready Django web application that predicts medical insurance costs using machine learning. This application uses a Random Forest regression model trained on medical insurance data to provide accurate cost estimates based on personal and health factors.

## 🌟 Features

- **Modern UI/UX**: Responsive, mobile-friendly interface with Bootstrap 5
- **Real-time Predictions**: Instant AI-powered cost estimates
- **Form Validation**: Comprehensive input validation with user-friendly error messages
- **Sample Data**: One-click sample data for easy testing
- **Error Handling**: Robust error handling and logging
- **Professional Design**: Modern gradients, animations, and transitions
- **Mobile Responsive**: Works seamlessly on all device sizes

## 📊 ML Model Details

- **Algorithm**: Random Forest Regressor
- **Training Accuracy**: ~97.68%
- **Test Accuracy**: ~83.0%
- **Features Used**:
  - Age (18-100 years)
  - Gender (Male/Female)
  - BMI (Body Mass Index, 10-50)
  - Number of Children (0-10)
  - Smoking Status (Smoker/Non-smoker)
  - Region (Northeast, Northwest, Southeast, Southwest)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "d:\project_learning\Machine_Learning\medical_cost_prediction\mysite"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`

## 🛠️ Development Setup

### Project Structure

```
medical_cost_prediction/
├── mysite/
│   ├── manage.py                 # Django management script
│   ├── requirements.txt         # Python dependencies
│   ├── mysite/
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # Main URL configuration
│   │   └── wsgi.py             # WSGI configuration
│   └── polls/
│       ├── views.py            # Main application logic
│       ├── urls.py             # App URL configuration
│       ├── templates/
│       │   └── index.html      # Main template
│       └── Medical.pickle      # Trained ML model
└── Medical cost.csv            # Training dataset
```

### Dependencies

- **Django 4.2.7**: Web framework
- **scikit-learn 1.3.2**: Machine learning library
- **pandas 2.0.3**: Data manipulation
- **numpy 1.24.3**: Numerical computing
- **Bootstrap 5**: Frontend framework (via CDN)
- **Font Awesome 6**: Icons (via CDN)

## 📝 API Usage

### Prediction Endpoint

**URL**: `/` (POST request)

**Parameters**:
- `name`: Full name (string)
- `age`: Age (integer, 18-100)
- `sex`: Gender (0=Female, 1=Male)
- `bmi`: BMI (float, 10-50)
- `child`: Number of children (integer, 0-10)
- `smoker`: Smoking status (0=Non-smoker, 1=Smoker)
- `region`: Region (0=Northeast, 1=Northwest, 2=Southeast, 3=Southwest)

**Response**: Returns predicted annual medical insurance cost in USD

## 🧪 Testing

### Manual Testing

1. **Start the application**: `python manage.py runserver`
2. **Open browser**: Navigate to `http://127.0.0.1:8000/`
3. **Test with sample data**: Click the "Sample Data" button to auto-fill the form
4. **Submit prediction**: Click "Predict Cost" to get results
5. **Test validation**: Try invalid inputs to see error handling

### Test Cases

- **Valid input**: All fields filled with valid ranges
- **Invalid age**: Age < 18 or > 100
- **Invalid BMI**: BMI < 10 or > 50
- **Invalid children**: Negative number or > 10
- **Empty fields**: Missing required fields
- **Model loading**: Test with/without Medical.pickle file

## 🔧 Configuration

### Django Settings

Key settings in `mysite/settings.py`:
- `DEBUG = True` (development mode)
- `ALLOWED_HOSTS = ['127.0.0.1', 'localhost']`
- `SECRET_KEY`: Change for production

### Production Deployment

For production deployment:

1. **Set DEBUG to False**:
   ```python
   DEBUG = False
   ```

2. **Update ALLOWED_HOSTS**:
   ```python
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

3. **Set secure SECRET_KEY**:
   ```python
   SECRET_KEY = 'your-secure-secret-key'
   ```

4. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

5. **Use production server** (Gunicorn):
   ```bash
   gunicorn mysite.wsgi:application
   ```

## 🐛 Troubleshooting

### Common Issues

1. **Model file not found**:
   - Ensure `Medical.pickle` exists in `polls/` directory
   - Check file permissions

2. **Django server won't start**:
   - Check if port 8000 is in use
   - Verify all dependencies are installed
   - Run `python manage.py check` for diagnostics

3. **Prediction errors**:
   - Verify input data ranges
   - Check model file integrity
   - Review Django logs for errors

4. **UI not loading properly**:
   - Check internet connection (Bootstrap/Font Awesome from CDN)
   - Verify template syntax
   - Check browser console for JavaScript errors

### Logging

The application uses Django's logging framework. Check logs for:
- Model loading errors
- Prediction failures
- Form validation issues

## 📈 Model Performance

The Random Forest model was trained on 1,329 samples with the following performance:
- **Training R² Score**: 0.9768 (97.68%)
- **Test R² Score**: 0.8300 (83.0%)
- **Features**: 6 predictive variables
- **Target**: Medical insurance charges (USD)

### Feature Importance

Based on the training data, the most influential factors for medical insurance costs are:
1. **Smoking status** (highest impact)
2. **Age**
3. **BMI**
4. **Number of children**
5. **Region**
6. **Gender**

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and demonstration purposes. Please ensure compliance with any applicable licenses when using in production.

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review Django logs for error details
- Verify all dependencies are properly installed

---

**Note**: This application provides estimates based on historical data and should not be used as the sole basis for insurance decisions. Actual costs may vary based on additional factors not included in this model.
