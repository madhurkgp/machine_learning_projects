# Bank Credit Card Prediction - ML Web Application

A production-ready Django web application that uses machine learning to predict the most suitable credit card category for bank customers based on their demographic and financial data.

## 🚀 Features

- **ML-Powered Predictions**: Advanced machine learning model analyzes customer data to predict credit card categories
- **Modern UI/UX**: Beautiful, responsive interface built with Bootstrap 5 and modern CSS
- **Real-time Validation**: Client-side and server-side form validation with user-friendly error messages
- **Sample Data**: One-click sample data filling for easy testing and demonstration
- **Mobile Responsive**: Fully responsive design that works on all devices
- **Error Handling**: Comprehensive error handling with informative feedback
- **Professional Design**: Clean, modern interface with gradients, animations, and transitions

## 🎯 Card Categories

The ML model predicts one of four credit card categories:
- **Blue**: Standard entry-level card
- **Gold**: Mid-tier premium card
- **Silver**: Alternative premium option
- **Platinum**: High-end luxury card

## 📊 ML Model Features

The model analyzes 20+ features including:

### Customer Demographics
- Age, Gender, Marital Status
- Education Level, Income Category
- Number of Dependents

### Banking Information
- Months on Book (customer tenure)
- Total Relationship Count
- Months Inactive, Contact Count
- Credit Limit, Revolving Balance

### Transaction Behavior
- Total Transaction Amount & Count
- Average Open to Buy
- Amount & Count Changes (Q4 to Q1)
- Average Utilization Ratio

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7 (Python)
- **Frontend**: Bootstrap 5, Font Awesome 6
- **ML Libraries**: scikit-learn 1.3.2, pandas 2.0.3, numpy 1.24.3
- **Database**: SQLite (development ready)
- **Deployment**: Gunicorn ready

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bank_customer_prediction/Code/mysite
   ```

2. **Create and activate virtual environment**
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
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000`

## 🔧 Configuration

### Development Settings
- `DEBUG = True` (enabled for local development)
- `ALLOWED_HOSTS` includes localhost and 127.0.0.1
- SQLite database for development

### Production Settings
For production deployment:
1. Set `DEBUG = False`
2. Update `ALLOWED_HOSTS` with your domain
3. Configure production database (PostgreSQL recommended)
4. Set up static files serving
5. Configure environment variables for sensitive data

## 📁 Project Structure

```
bank_customer_prediction/
├── Code/
│   └── mysite/
│       ├── manage.py              # Django management script
│       ├── mysite/
│       │   ├── settings.py        # Django settings
│       │   ├── urls.py           # Main URL configuration
│       │   └── wsgi.py           # WSGI configuration
│       ├── polls/
│       │   ├── views.py          # Main application logic
│       │   ├── urls.py           # App URL configuration
│       │   ├── templates/
│       │   │   └── index.html    # Main template
│       │   ├── BankCards.pickle  # Trained ML model
│       │   └── BankCardsPCA.pickle # PCA transformer
│       └── requirements.txt       # Python dependencies
└── Bank customers.csv            # Sample dataset
```

## 🤖 ML Model Details

### Model Architecture
- **PCA Dimensionality Reduction**: Reduces feature complexity while preserving variance
- **Classification Algorithm**: Optimized classifier for multi-class prediction
- **Feature Engineering**: Preprocessed categorical and numerical features

### Model Files
- `BankCardsPCA.pickle`: PCA transformer for dimensionality reduction
- `BankCards.pickle`: Trained classification model

### Input Features
The model expects 20 standardized features:
1. Attrition_Flag (0/1)
2. Customer_Age (18-100)
3. Gender (0: Female, 1: Male)
4. Dependent_count (0-10)
5. Education_Level (0-6)
6. Marital_Status (0-3)
7. Income_Category (0-5)
8. Months_on_book (0-120)
9. Total_Relationship_Count (0-10)
10. Months_Inactive_12_mon (0-12)
11. Contacts_Count_12_mon (0-20)
12. Credit_Limit (0+)
13. Total_Revolving_Bal (0+)
14. Avg_Open_To_Buy (0+)
15. Total_Amt_Chng_Q4_Q1 (0+)
16. Total_Trans_Amt (0+)
17. Total_Trans_Ct (0+)
18. Total_Ct_Chng_Q4_Q1 (0+)
19. Avg_Utilization_Ratio (0-1)

## 🧪 Testing

### Manual Testing
1. Use the "Fill Sample Data" button for quick testing
2. Test various input combinations
3. Verify error handling with invalid inputs
4. Check responsive design on different screen sizes

### Test Cases
- **Valid Input**: Complete all fields and verify prediction
- **Missing Fields**: Test validation errors
- **Invalid Values**: Test with out-of-range values
- **Edge Cases**: Test boundary values
- **Mobile View**: Test on mobile devices

## 🚀 Deployment

### Heroku Deployment
1. Install Heroku CLI
2. Create Procfile:
   ```
   web: gunicorn mysite.wsgi:application
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Model File Not Found**
   - Ensure `BankCards.pickle` and `BankCardsPCA.pickle` are in the `polls/` directory
   - Check file permissions

2. **Django Server Won't Start**
   - Verify all dependencies are installed
   - Check for port conflicts (default: 8000)

3. **Prediction Errors**
   - Ensure all form fields are filled
   - Check input value ranges
   - Verify model file integrity

4. **Static Files Not Loading**
   - Run `python manage.py collectstatic` for production
   - Check STATIC_URL and STATIC_ROOT settings

### Debug Mode
Enable debug mode for detailed error information:
```python
DEBUG = True
```

## 📈 Performance Optimization

### Database Optimization
- Use indexes for frequently queried fields
- Implement database connection pooling

### ML Model Optimization
- Consider model quantization for faster inference
- Implement model caching for repeated predictions

### Frontend Optimization
- Minimize CSS and JavaScript files
- Implement lazy loading for large datasets

## 🔒 Security Considerations

- Input validation and sanitization
- CSRF protection enabled
- Environment variables for sensitive data
- Regular security updates for dependencies

## 📝 API Documentation

### Main Endpoint
- **URL**: `/` (POST)
- **Purpose**: Predict credit card category
- **Method**: POST
- **Parameters**: Form data with customer features
- **Response**: Rendered HTML with prediction result

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

- **v2.0.0**: Complete UI/UX overhaul with modern design
- **v1.5.0**: Added error handling and validation
- **v1.0.0**: Initial release with basic ML prediction

---

**Built with ❤️ using Django and Machine Learning**
