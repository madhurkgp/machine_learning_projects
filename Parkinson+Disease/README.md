# Parkinson's Disease Prediction System

A production-ready Django web application that uses machine learning to predict Parkinson's disease based on voice analysis. This system analyzes various vocal measurements to provide accurate predictions with confidence scores.

## 🚀 Features

- **High Accuracy**: 92.3% accuracy using Decision Tree classifier
- **Modern UI**: Responsive, mobile-friendly interface with real-time validation
- **Sample Data**: Pre-loaded examples for easy testing
- **Real-time Predictions**: Instant results with probability breakdowns
- **Comprehensive Documentation**: Detailed information about voice analysis
- **Privacy-focused**: All data processed locally, no storage of personal information

## 🧬 About Parkinson's Disease Detection

Parkinson's disease often affects voice production before motor symptoms become apparent. Our system analyzes 22 different acoustic features including:

- **Frequency Measurements**: Average, maximum, and minimum vocal fundamental frequency
- **Jitter Measurements**: Variations in fundamental frequency
- **Shimmer Measurements**: Variations in amplitude  
- **Noise Measures**: Harmonic to noise ratios
- **Nonlinear Measures**: Complexity and fractal scaling properties

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Parkinson+Disease
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

4. **Train the ML model**
   ```bash
   python train_model.py
   ```
   This will create `parkinson_model.joblib` and `feature_names.joblib` files.

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000`

## 🎯 Quick Start

Once the server is running:

1. **Test with Sample Data**: Click "Load Healthy Sample" or "Load Parkinson's Sample" buttons
2. **Enter Custom Data**: Fill in the 22 voice measurement fields
3. **Get Prediction**: Click "Predict Parkinson's Disease" for instant results
4. **View Results**: See prediction with confidence scores and probability breakdowns

## 📊 Model Performance

- **Algorithm**: Decision Tree Classifier
- **Accuracy**: 92.3% on test set
- **Dataset**: Oxford Parkinson's Disease Detection Dataset
- **Training Samples**: 195 voice recordings (31 individuals)
- **Features**: 22 acoustic measurements

### Feature Importance (Top 5)
1. Spread1 (-8 to -2): 85%
2. PPE (Pitch Period Entropy): 78%
3. MDVP:Fo (Average Frequency): 72%
4. DFA (Detrended Fluctuation): 65%
5. RPDE (Recurrence Density): 60%

## 🏗️ Project Structure

```
Parkinson+Disease/
├── parkinson_app/          # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
├── predictor/             # Django app for predictions
│   ├── views.py          # Main prediction logic
│   ├── forms.py          # Form validation and data processing
│   ├── urls.py           # App URL routing
│   └── templates/        # HTML templates
├── static/               # CSS, JavaScript, and static files
│   ├── css/style.css     # Custom styling
│   └── js/main.js        # Frontend functionality
├── templates/            # Base templates
├── train_model.py        # ML model training script
├── parkinson_model.joblib # Trained ML model
├── feature_names.joblib  # Feature names for model
├── parkinsons.data       # Original dataset
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

## 🔧 Configuration

### Environment Variables

The application uses Django's built-in settings. Key configurations in `parkinson_app/settings.py`:

- `DEBUG=True` for development (set to `False` for production)
- `ALLOWED_HOSTS=[]` - add your domain for production
- `STATIC_URL='static/'` - static files configuration

### Model Retraining

To retrain the model with new data:

1. Update `parkinsons.data` with your dataset
2. Run `python train_model.py`
3. Restart the Django server

## 🧪 Testing

### Manual Testing

1. **Form Validation**: Test empty fields and invalid ranges
2. **Sample Data**: Verify both healthy and Parkinson's samples
3. **Custom Input**: Test with known values from the dataset
4. **Error Handling**: Verify error messages display correctly

### Sample Test Cases

**Healthy Case Expected Result:**
```
Prediction: Healthy
Confidence: ~95%
Probabilities: Healthy ~95%, Parkinson's ~5%
```

**Parkinson's Case Expected Result:**
```
Prediction: Parkinson's Disease  
Confidence: ~90%
Probabilities: Healthy ~10%, Parkinson's ~90%
```

## 🚀 Deployment

### Production Setup

1. **Set environment variables**:
   ```bash
   export DEBUG=False
   export ALLOWED_HOSTS=['yourdomain.com']
   ```

2. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Use production server** (Gunicorn recommended):
   ```bash
   pip install gunicorn
   gunicorn parkinson_app.wsgi:application
   ```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python train_model.py
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "parkinson_app.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📚 API Endpoints

- `GET /` - Home page with prediction form
- `POST /predict/` - Process prediction request
- `GET /sample-data/` - Get sample data for testing
- `GET /about/` - About page with detailed information

### Prediction API Response

**Success Response**:
```json
{
  "success": true,
  "prediction": 1,
  "prediction_label": "Parkinson's Disease",
  "confidence": 89.5,
  "probabilities": {
    "healthy": 10.5,
    "parkinsons": 89.5
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Validation error",
  "errors": {
    "mdvp_fo": ["Please enter a valid value between 50 and 300"]
  }
}
```

## 🔒 Security Considerations

- **No Data Storage**: All voice measurements are processed in memory only
- **Input Validation**: Server-side validation for all input fields
- **CSRF Protection**: Django's built-in CSRF protection enabled
- **Privacy**: No personal information is collected or stored

## ⚠️ Medical Disclaimer

**IMPORTANT**: This tool is for educational and research purposes only and should NOT be used as a substitute for professional medical diagnosis, treatment, or advice. Always consult qualified healthcare professionals for medical concerns.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add feature description'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Dataset Source**: Oxford Parkinson's Disease Detection Dataset
- **Research**: Max A. Little et al., University of Oxford
- **Original Study**: "Suitability of dysphonia measurements for telemonitoring of Parkinson's disease" (IEEE Transactions on Biomedical Engineering, 2008)

## 📞 Support

For questions or issues:

1. Check the troubleshooting section below
2. Review the [Issues](../../issues) page
3. Create a new issue with detailed information

## 🔧 Troubleshooting

### Common Issues

**Model not loading error:**
```bash
# Solution: Train the model
python train_model.py
```

**Static files not loading:**
```bash
# Solution: Collect static files
python manage.py collectstatic
```

**Port already in use:**
```bash
# Solution: Use different port
python manage.py runserver 8001
```

**Template not found:**
- Ensure `predictor/templates/predictor/` directory exists
- Check Django settings for TEMPLATES configuration

**Form validation errors:**
- Verify all required fields are filled
- Check values are within specified ranges
- Ensure JavaScript is enabled in browser

### Performance Optimization

For production deployment:

1. **Enable caching**: Configure Redis or Memcached
2. **Use CDN**: Serve static files via CDN
3. **Database optimization**: Use PostgreSQL for production
4. **Load balancing**: Deploy multiple instances behind load balancer

## 📈 Future Enhancements

- **Deep Learning Models**: Implement LSTM or CNN for better accuracy
- **Mobile App**: React Native app for voice recording
- **Longitudinal Tracking**: Monitor disease progression over time
- **Multi-language Support**: Support for different languages
- **Integration**: Connect with electronic health records

---

**Built with ❤️ using Django, scikit-learn, and modern web technologies**
