# Customer Churn Prediction Web Application

A production-ready Django web application that predicts customer churn using a trained Random Forest machine learning model. This application provides an intuitive interface for businesses to analyze customer data and get real-time churn predictions.

## Features

- **Advanced ML Model**: Random Forest classifier with 87.55% accuracy
- **Modern UI**: Responsive, mobile-friendly interface with gradient designs
- **Real-time Predictions**: Instant churn probability calculations
- **Form Validation**: Client-side and server-side validation for all inputs
- **Sample Data**: One-click sample data loading for easy testing
- **Risk Assessment**: Detailed risk levels (Low, Medium, High) with confidence scores
- **Professional Design**: Modern CSS with animations and transitions

## Technology Stack

- **Backend**: Django 4.2.7
- **Machine Learning**: Scikit-learn 1.3.2 (Random Forest)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Data Processing**: Pandas 2.1.3, NumPy 1.24.3
- **Model Serialization**: Joblib 1.3.2
- **Deployment Ready**: Gunicorn, Whitenoise

## Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone or Download the Project**
   ```bash
   # Navigate to the project directory
   cd "Customer+churn+files"
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the ML Model** (if not already trained)
   ```bash
   python train_model.py
   ```
   This will:
   - Load the dataset from `Notebook/Churn Modeling.csv`
   - Train a Random Forest model
   - Save the model and artifacts to the `models/` directory

5. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   Open your browser and navigate to: `http://127.0.0.1:8000`

## Project Structure

```
Customer+churn+files/
|
|-- churn_prediction_app/          # Django project settings
|   |-- settings.py               # Django configuration
|   |-- urls.py                   # Main URL routing
|   |-- wsgi.py                   # WSGI configuration
|
|-- prediction/                   # Django app for predictions
|   |-- views.py                  # ML integration and view logic
|   |-- urls.py                   # App URL routing
|   |-- templates/prediction/
|   |   |-- home.html            # Main application interface
|
|-- models/                       # Trained ML models and artifacts
|   |-- random_forest_model.pkl   # Serialized Random Forest model
|   |-- label_encoder.pkl         # Fitted label encoder
|   |-- feature_names.pkl        # Model feature names
|
|-- static/                       # Static assets
|   |-- css/style.css             # Application styles
|   |-- js/app.js                 # Frontend JavaScript
|
|-- templates/                    # Django templates
|-- Notebook/                     # Original ML notebook and data
|   |-- Customer Churning Prediction.ipynb
|   |-- Churn Modeling.csv
|
|-- requirements.txt              # Python dependencies
|-- train_model.py               # Model training script
|-- manage.py                    # Django management script
|-- README.md                    # This documentation
```

## API Endpoints

### 1. Home Page
- **URL**: `/`
- **Method**: GET
- **Description**: Renders the main prediction interface

### 2. Predict Churn
- **URL**: `/predict/`
- **Method**: POST
- **Content-Type**: `application/json`
- **Description**: Processes customer data and returns churn prediction

**Request Body**:
```json
{
    "credit_score": 650,
    "geography": "France",
    "gender": "Female",
    "age": 42,
    "tenure": 5,
    "balance": 75000,
    "num_products": 2,
    "has_cr_card": 1,
    "is_active_member": 1,
    "estimated_salary": 100000
}
```

**Response**:
```json
{
    "prediction": 0,
    "confidence": 85.5,
    "risk_level": "Low",
    "result_text": "Customer is likely to stay",
    "probability_churn": 14.5,
    "probability_stay": 85.5
}
```

### 3. Sample Data
- **URL**: `/sample-data/`
- **Method**: GET
- **Description**: Returns sample customer data for testing

## Model Details

### Algorithm
- **Type**: Random Forest Classifier
- **Estimators**: 100 trees
- **Features**: 10 customer attributes
- **Training Data**: 10,000 customer records
- **Test Accuracy**: 87.55%
- **ROC AUC Score**: 73.24%

### Features Used
1. CreditScore (300-850)
2. Geography (France, Germany, Spain)
3. Gender (Male, Female)
4. Age (18-100)
5. Tenure (0-10 years)
6. Account Balance ($)
7. Number of Products (1-4)
8. Has Credit Card (Yes/No)
9. Is Active Member (Yes/No)
10. Estimated Salary ($)

### Input Validation
- Credit Score: 300-850
- Age: 18-100 years
- Tenure: 0-10 years
- Balance: Non-negative
- Number of Products: 1-4
- Estimated Salary: Non-negative

## Usage Guide

### Making Predictions

1. **Fill Customer Information**:
   - Enter credit score, geography, gender, and age
   - All fields marked with * are required

2. **Provide Account Details**:
   - Input tenure, balance, number of products, and estimated salary
   - Use realistic values within the specified ranges

3. **Set Account Status**:
   - Check if the customer has a credit card
   - Check if the customer is an active member

4. **Get Prediction**:
   - Click "Predict Churn" to analyze the data
   - View results with confidence scores and risk levels

### Sample Data Testing
- Click "Load Sample Data" to auto-fill the form with test values
- This helps you understand the expected input format

### Understanding Results
- **Low Risk**: Customer likely to stay (green badge)
- **Medium Risk**: Moderate churn probability (yellow badge)
- **High Risk**: Customer likely to churn (red badge)
- **Confidence**: Model's prediction certainty
- **Probabilities**: Detailed churn vs retention percentages

## Deployment

### Production Deployment

1. **Environment Setup**:
   ```bash
   export DEBUG=False
   export ALLOWED_HOSTS='yourdomain.com'
   export SECRET_KEY='your-secret-key'
   ```

2. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Use Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn churn_prediction_app.wsgi:application
   ```

4. **Configure Web Server**:
   - Set up Nginx or Apache as reverse proxy
   - Configure SSL certificates
   - Set up proper logging

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python train_model.py
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "churn_prediction_app.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Troubleshooting

### Common Issues

1. **Model Not Loading**:
   - Ensure `train_model.py` has been run
   - Check that `models/` directory contains the pickle files
   - Verify file permissions

2. **Server Not Starting**:
   - Check if port 8000 is available
   - Ensure all dependencies are installed
   - Run `python manage.py check` for configuration issues

3. **Prediction Errors**:
   - Verify all input fields are filled correctly
   - Check input values are within valid ranges
   - Ensure categorical values match expected options

4. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check STATIC_URL and STATIC_ROOT settings
   - Verify file permissions in static directory

### Debug Mode

Enable debug mode for detailed error messages:
```python
# In churn_prediction_app/settings.py
DEBUG = True
```

### Logs

Check Django logs for detailed error information:
```bash
python manage.py runserver --verbosity=2
```

## Performance Optimization

### Model Optimization
- The Random Forest model is optimized for both accuracy and speed
- Prediction time: < 100ms per request
- Memory usage: ~50MB for loaded model

### Caching
- Consider implementing Redis caching for frequent predictions
- Cache static model predictions for similar customer profiles

### Database
- Currently uses SQLite for simplicity
- For production, consider PostgreSQL or MySQL
- Implement connection pooling for better performance

## Security Considerations

- Input validation prevents SQL injection and XSS attacks
- CSRF protection enabled for all forms
- No sensitive customer data is stored permanently
- Model files are not accessible via web server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and demonstration purposes. Please ensure compliance with your organization's data usage policies when implementing in production.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the Django and Scikit-learn documentation
3. Verify all dependencies are correctly installed

---

**Built with Django, Scikit-learn, and modern web technologies**
