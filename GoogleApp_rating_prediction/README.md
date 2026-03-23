# Google App Rating Predictor 🌟

A production-ready Django web application that predicts Google Play Store app ratings using machine learning algorithms. This application uses a trained regression model with PCA (Principal Component Analysis) to analyze app characteristics and predict potential ratings.

## 🚀 Features

- **Modern UI/UX**: Beautiful, responsive interface with Bootstrap 5 and custom CSS animations
- **ML Integration**: Advanced machine learning model for accurate rating predictions
- **Form Validation**: Client-side and server-side validation for data integrity
- **Sample Data**: One-click sample data filling for easy testing
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Mobile Responsive**: Fully responsive design that works on all devices
- **Real-time Results**: Instant rating predictions with visual star ratings

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd GoogleApp_rating_prediction
```

### 2. Navigate to the Project Directory

```bash
cd Code/mysite
```

### 3. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📊 Model Details

### Machine Learning Pipeline

1. **Data Preprocessing**: The model processes app features including:
   - Category (encoded)
   - App Size (MB)
   - Number of Installs
   - App Type (Free/Paid)
   - Price
   - Content Rating
   - Release Date (Year, Month, Day)

2. **Feature Engineering**: PCA (Principal Component Analysis) is applied to reduce dimensionality and extract the most important features.

3. **Regression Model**: A trained regression model predicts the app rating on a scale of 1.0 to 5.0.

### Model Files

- `AppsPCA.pickle`: PCA transformer for feature reduction
- `Apps.pickle`: Trained regression model

### Supported Categories

The model supports the following app categories:
- FAMILY
- GAME
- TOOLS
- MEDICAL
- LIFESTYLE
- PERSONALIZATION
- FINANCE
- SPORTS
- BUSINESS
- PHOTOGRAPHY
- PRODUCTIVITY
- HEALTH AND FITNESS
- COMMUNICATION

## 🎯 Usage Guide

### Making a Prediction

1. **Fill in App Details**:
   - Enter your app name
   - Select the appropriate category
   - Specify app size in MB
   - Enter the number of installs
   - Choose app type (Free/Paid)
   - Set the price (0.00 for free apps)
   - Select content rating
   - Provide release date

2. **Get Prediction**:
   - Click "Predict Rating" button
   - View the predicted rating with star display
   - Try different scenarios using "Try Another App"

### Sample Data Feature

Click the "Fill Sample Data" button to automatically populate the form with example values for testing purposes.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root for production:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Production Settings

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS` with your domain
3. Set up a proper database (PostgreSQL recommended)
4. Configure static files serving
5. Set up HTTPS

## 📁 Project Structure

```
GoogleApp_rating_prediction/
├── Code/
│   └── mysite/
│       ├── manage.py
│       ├── mysite/
│       │   ├── __init__.py
│       │   ├── settings.py
│       │   ├── urls.py
│       │   ├── asgi.py
│       │   └── wsgi.py
│       ├── polls/
│       │   ├── __init__.py
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── models.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   ├── templates/
│       │   │   └── index.html
│       │   ├── AppsPCA.pickle    # PCA model
│       │   └── Apps.pickle      # Regression model
│       └── requirements.txt
├── googleplaystore.csv          # Dataset (for reference)
├── Google Apps.ipynb           # Jupyter notebook (for reference)
└── README.md
```

## 🧪 Testing

### Running Tests

```bash
python manage.py test
```

### Manual Testing

1. **Form Validation**: Test with empty fields, invalid inputs
2. **Model Prediction**: Test with various app characteristics
3. **Error Handling**: Test with malformed data
4. **Responsive Design**: Test on different screen sizes

### Sample Test Cases

| Category | Size (MB) | Installs | Type | Price | Expected Range |
|----------|-----------|----------|------|-------|---------------|
| GAME | 25.5 | 500000 | Free | 0.00 | 3.5-4.5 |
| PRODUCTIVITY | 15.2 | 1000000 | Free | 0.00 | 4.0-4.8 |
| FINANCE | 45.8 | 100000 | Paid | 4.99 | 3.0-4.0 |

## 🐛 Troubleshooting

### Common Issues

1. **Model Files Not Found**
   - Ensure `AppsPCA.pickle` and `Apps.pickle` are in the `polls` directory
   - Check file permissions

2. **Django Server Won't Start**
   - Check if port 8000 is available
   - Verify virtual environment is activated
   - Ensure all dependencies are installed

3. **Prediction Errors**
   - Verify all form fields are filled correctly
   - Check for invalid data types
   - Ensure model files are not corrupted

4. **Static Files Not Loading**
   - Run `python manage.py collectstatic` for production
   - Check `STATIC_URL` and `STATIC_ROOT` settings

### Error Messages

- **"ML model files not found"**: Check that model files exist in the correct location
- **"Invalid input format"**: Verify all numeric fields contain valid numbers
- **"Please fill in all fields"**: Complete all required form fields

## 📈 Performance Considerations

- Model loading happens once per request
- Consider caching for high-traffic deployments
- Monitor memory usage with large datasets
- Optimize static file serving in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

## 🔄 Version History

- **v2.0.0**: Complete UI/UX overhaul, modern Django implementation
- **v1.0.0**: Initial release with basic ML functionality

---

**Built with ❤️ using Django, Bootstrap 5, and Machine Learning**
