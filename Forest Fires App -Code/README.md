# 🔥 Forest Fire Prediction System

An advanced Django-based web application that uses machine learning to predict forest fire confidence scores based on satellite data and environmental parameters.

## 🚀 Features

- **Real-time Prediction**: Instant confidence score calculation using a trained Random Forest model
- **Modern UI**: Beautiful, responsive interface built with Bootstrap 5
- **Comprehensive Input Parameters**: 
  - Geographic coordinates (latitude/longitude)
  - Fire characteristics (brightness, FRP)
  - Environmental conditions (day/night, scan level)
  - Temporal information (date, month, year)
  - Fire type classification
- **Professional Design**: Gradient backgrounds, smooth animations, and intuitive user experience

## 🛠 Technology Stack

- **Backend**: Django 4.2.7
- **Machine Learning**: Scikit-learn 1.3.0 (Random Forest Regressor)
- **Data Processing**: Pandas 2.0.3, NumPy 1.24.3
- **Frontend**: Bootstrap 5.3.0, HTML5, CSS3
- **Database**: SQLite3
- **Deployment**: Gunicorn (production ready)

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "Forest Fires App -Code/mysite"
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000`

## 🎯 Usage Guide

1. **Fill in the form** with the following parameters:
   - **Location**: Enter latitude and longitude coordinates
   - **Fire Characteristics**: 
     - Brightness/Intensity (300-600 range)
     - Fire Radiative Power (FRP) value
   - **Environmental Conditions**:
     - Select Day or Night
     - Choose appropriate Scan Level
   - **Temporal Information**:
     - Select Fire Type (Type 0, 2, or 3)
     - Enter Year, Month, and Date

2. **Click "Predict Fire Confidence"** to get your results

3. **View the confidence score** displayed as a percentage with professional styling

## 🤖 Machine Learning Model

The application uses a **Random Forest Regressor** model trained on satellite fire detection data with the following features:

- **Training Dataset**: 36,011 fire incidents
- **Model Performance**: 
  - Training accuracy: ~95%
  - Testing accuracy: ~65%
- **Features Used**:
  - Geographic coordinates
  - Brightness and thermal measurements
  - Satellite scan parameters
  - Temporal features
  - Fire classification types

## 📊 Input Parameters Explained

| Parameter | Description | Range/Options |
|-----------|-------------|---------------|
| **Latitude** | Geographic latitude coordinate | -90 to 90 |
| **Longitude** | Geographic longitude coordinate | -180 to 180 |
| **Brightness** | Fire brightness intensity | 300-600 |
| **FRP** | Fire Radiative Power | Numeric value |
| **Day/Night** | Time of detection | Day (1) or Night (0) |
| **Scan Level** | Satellite scan resolution | 1-5 (binned ranges) |
| **Fire Type** | Classification of fire source | Type 0, 2, or 3 |
| **Year/Month/Date** | Temporal information | Valid date ranges |

## 🎨 Design Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI Elements**:
  - Gradient backgrounds
  - Smooth hover effects
  - Professional typography
  - Intuitive form sections
- **User Experience**:
  - Input validation
  - Helpful placeholders
  - Clear section organization
  - Visual feedback for results

## 🔧 Configuration

### Development Settings
- `DEBUG = True` (enabled for development)
- `ALLOWED_HOSTS` includes localhost and 127.0.0.1
- SQLite database for development

### Production Deployment
For production deployment:
1. Set `DEBUG = False` in `settings.py`
2. Update `ALLOWED_HOSTS` with your domain
3. Configure proper database settings
4. Set up static file serving
5. Use environment variables for sensitive data

## 📁 Project Structure

```
mysite/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3              # SQLite database
├── mysite/                 # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
└── polls/                  # Main application
    ├── views.py           # Main logic and ML prediction
    ├── templates/         # HTML templates
    │   └── index.html    # Main interface
    ├── ForestModel.bz2   # Trained ML model
    └── urls.py           # App URL routing
```

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Error**:
   - Ensure `ForestModel.bz2` exists in the `polls/` directory
   - Check file permissions

2. **Dependencies Issues**:
   - Make sure virtual environment is activated
   - Install exact versions from `requirements.txt`

3. **Django Server Issues**:
   - Check if port 8000 is available
   - Try running with `python manage.py runserver 0.0.0.0:8000`

4. **Form Validation Errors**:
   - Ensure all required fields are filled
   - Check numeric ranges for input fields

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **NASA FIRMS**: For providing the fire detection dataset
- **Scikit-learn**: For the machine learning framework
- **Django**: For the robust web framework
- **Bootstrap**: For the responsive UI components

## 📞 Support

For any questions or issues, please:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

---

**🔥 Stay safe and help prevent forest fires!**
