# Sentiment Analysis Web Application

A production-ready Django web application that analyzes text sentiment using machine learning. Built with Python, Django, and scikit-learn.

## 🚀 Features

- **Real-time Sentiment Analysis**: Analyze text for positive, negative, or neutral sentiment
- **Machine Learning Model**: Uses Logistic Regression with TF-IDF vectorization
- **Modern UI**: Responsive, mobile-friendly interface with Bootstrap 5
- **API Endpoints**: RESTful API for programmatic access
- **History Tracking**: View and paginate through past predictions
- **Sample Data**: Built-in sample texts for easy testing
- **Admin Interface**: Django admin for managing predictions
- **Form Validation**: Client and server-side validation with user-friendly error messages

## 📋 Requirements

- Python 3.8+
- Django 4.2+
- scikit-learn
- pandas
- numpy
- nltk

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sentiment_analysis
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

4. **Setup database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the application**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Web Interface: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 🏗️ Project Structure

```
sentiment_analysis/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── sentiment_web/           # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── prediction/              # Main Django app
│   ├── __init__.py
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration
│   ├── forms.py             # Django forms
│   ├── models.py            # Database models
│   ├── ml_model.py          # Machine learning model
│   ├── urls.py              # App URL routing
│   ├── views.py             # View functions
│   ├── migrations/          # Database migrations
│   └── templates/prediction/ # HTML templates
│       ├── base.html        # Base template
│       ├── home.html        # Home page
│       ├── result.html      # Results page
│       └── history.html     # History page
├── static/                  # Static files
│   └── css/
│       └── custom.css       # Custom CSS
├── models/                  # Trained ML models (auto-created)
├── Notebook/                # Original ML notebooks and data
│   ├── SentimentAnalysis.ipynb
│   ├── contractions.py
│   ├── nlp_utils.py
│   └── TextAnalytics.txt    # Training data
└── media/                   # User uploaded files (auto-created)
```

## 🔧 Configuration

### Environment Variables

The application uses Django's built-in settings. For production, consider:

- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Set a secure `SECRET_KEY`
- Configure database settings
- Set up static file serving

### Model Training

The ML model is automatically trained on first run using the dataset in `Notebook/TextAnalytics.txt`. The trained model and vectorizer are saved in the `models/` directory.

## 📊 API Endpoints

### Analyze Sentiment
- **URL**: `/api/predict/`
- **Method**: POST
- **Content-Type**: application/json
- **Request Body**:
  ```json
  {
    "text": "Your text to analyze"
  }
  ```
- **Response**:
  ```json
  {
    "prediction": "Positive",
    "confidence": 85.5,
    "id": 123
  }
  ```

### Get Sample Texts
- **URL**: `/api/samples/`
- **Method**: GET
- **Response**:
  ```json
  {
    "samples": [
      "Sample text 1...",
      "Sample text 2..."
    ]
  }
  ```

## 🧪 Testing

### Manual Testing

1. **Basic Functionality**
   - Navigate to http://127.0.0.1:8000/
   - Enter text in the form
   - Click "Analyze Sentiment"
   - Verify results display correctly

2. **Sample Text Testing**
   - Click "Sample Text" button
   - Select a sample text
   - Verify it populates the form

3. **History Testing**
   - Make a few predictions
   - Navigate to History tab
   - Verify pagination works

4. **API Testing**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/predict/ \
        -H "Content-Type: application/json" \
        -d '{"text": "This is a great movie!"}'
   ```

### Unit Tests

Run the Django test suite:
```bash
python manage.py test
```

## 🐛 Troubleshooting

### Common Issues

1. **NLTK Data Download Errors**
   - The application automatically downloads required NLTK data
   - If errors persist, manually download:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   nltk.download('averaged_perceptron_tagger')
   ```

2. **Model Training Fails**
   - Ensure `Notebook/TextAnalytics.txt` exists
   - Check file permissions
   - Verify data format (label,text with comma separator)

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATIC_ROOT` settings

4. **Server Won't Start**
   - Check if port 8000 is available
   - Try different port: `python manage.py runserver 8080`
   - Verify all dependencies are installed

### Performance Optimization

For production deployment:

1. **Database Optimization**
   - Use PostgreSQL instead of SQLite
   - Add database indexes
   - Implement connection pooling

2. **Caching**
   - Configure Redis or Memcached
   - Cache ML model predictions
   - Cache static assets

3. **Static File Serving**
   - Use nginx or CDN for static files
   - Enable gzip compression
   - Implement browser caching

## 🚀 Deployment

### Production Deployment Checklist

1. **Security**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for sensitive data
   - Enable HTTPS

2. **Database**
   - Migrate to PostgreSQL
   - Set up database backups
   - Configure connection pooling

3. **Web Server**
   - Use Gunicorn or uWSGI
   - Configure nginx as reverse proxy
   - Set up SSL certificates

4. **Monitoring**
   - Implement logging
   - Set up error tracking
   - Monitor performance metrics

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sentiment_web.wsgi:application"]
```

## 📈 Model Performance

The current model achieves:
- **Accuracy**: ~85% on the training dataset
- **Features**: TF-IDF vectorization with 5000 max features
- **Algorithm**: Logistic Regression with L2 regularization
- **Preprocessing**: Text cleaning, tokenization, stopword removal, lemmatization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

---

**Built with ❤️ using Django and Machine Learning**
