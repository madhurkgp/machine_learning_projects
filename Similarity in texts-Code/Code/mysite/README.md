# Text Similarity Analyzer

A production-ready Django web application that analyzes semantic similarity between two texts using advanced machine learning algorithms and word embeddings.

## 🚀 Features

- **Modern UI/UX**: Clean, responsive design with gradient backgrounds and smooth animations
- **Real-time Analysis**: Instant similarity calculation using word embeddings
- **Visual Feedback**: Progress bars and similarity scores with intuitive interpretations
- **Sample Data**: Built-in sample texts for easy testing and demonstration
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Mobile Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- **Processing Visualization**: Shows processed text after stopwords removal and cleaning

## 🛠 Technology Stack

- **Backend**: Django 4.2.7
- **Machine Learning**: 
  - NLTK for text preprocessing
  - NumPy for vector operations
  - Custom word embeddings (50-dimensional vectors)
  - Cosine similarity algorithm
- **Frontend**: HTML5, CSS3, JavaScript (no external frameworks)
- **Database**: SQLite (development)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "Similarity in texts-Code/Code/mysite"
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK Data

```bash
python -c "import nltk; nltk.download('stopwords')"
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

### 7. Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

## 📖 Usage

### Basic Usage

1. **Enter Text**: Type or paste your first text in the "First Text" field
2. **Enter Second Text**: Type or paste your second text in the "Second Text" field
3. **Click Analyze**: Press the "Analyze Similarity" button
4. **View Results**: See the similarity score and interpretation

### Using Sample Texts

Click on any sample text pair in the "Sample Texts for Testing" section to automatically fill the form with example texts.

### Understanding Results

- **0.8 - 1.0**: Very High Similarity - Texts are extremely similar
- **0.6 - 0.8**: High Similarity - Texts share many common concepts
- **0.4 - 0.6**: Moderate Similarity - Texts have some common elements
- **0.2 - 0.4**: Low Similarity - Texts are somewhat related
- **0.0 - 0.2**: Very Low Similarity - Texts are quite different

## 🔧 How It Works

### Text Preprocessing

1. **HTML Cleaning**: Removes HTML tags and entities
2. **URL Removal**: Eliminates web URLs and email addresses
3. **Character Cleaning**: Removes special characters and normalizes whitespace
4. **Case Normalization**: Converts all text to lowercase
5. **Stopword Removal**: Removes common English stopwords (the, a, an, etc.)

### Similarity Calculation

1. **Word Embedding**: Each word is converted to a 50-dimensional vector
2. **Document Vector**: Text vectors are summed to create document representations
3. **Cosine Similarity**: Calculates the cosine of the angle between document vectors
4. **Normalization**: Results are normalized to a 0-1 scale

### Error Handling

- **Empty Input**: Validates that both text fields are filled
- **Model Loading**: Handles cases where the word embedding model fails to load
- **Processing Errors**: Catches and displays any errors during text processing
- **Vector Norm**: Handles cases where text vectors have zero magnitude

## 📁 Project Structure

```
mysite/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3               # SQLite database
├── mysite/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
└── polls/                   # Main application
    ├── __init__.py
    ├── admin.py             # Django admin configuration
    ├── apps.py              # Application configuration
    ├── models.py            # Database models
    ├── views.py             # View logic
    ├── utils.py             # Text processing utilities
    ├── urls.py              # Application URLs
    ├── templates/           # HTML templates
    │   └── index.html       # Main page template
    ├── templatetags/        # Custom template filters
    │   ├── __init__.py
    │   └── custom_filters.py
    ├── migrations/          # Database migrations
    └── word_embeddings_smaller.pickle  # Word embedding model
```

## 🧪 Testing

### Manual Testing

1. **Basic Functionality Test**:
   - Enter two similar texts (e.g., "Machine learning is great" and "ML is wonderful")
   - Expected: High similarity score (>0.6)

2. **Different Texts Test**:
   - Enter two unrelated texts (e.g., "The sky is blue" and "Cars have wheels")
   - Expected: Low similarity score (<0.3)

3. **Edge Cases**:
   - Empty fields should show validation errors
   - Very short texts should still work
   - Special characters should be handled properly

### Sample Test Cases

```python
# High Similarity
text1 = "Machine learning is a subset of artificial intelligence"
text2 = "AI systems can learn automatically from data"
# Expected: > 0.6

# Low Similarity  
text1 = "The weather is sunny today"
text2 = "Stock markets are volatile this week"
# Expected: < 0.2
```

## 🔒 Security Considerations

- Input validation prevents empty submissions
- Text preprocessing removes potentially harmful content
- No user data is stored permanently
- CSRF protection enabled
- Debug mode disabled in production

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**:
   ```bash
   export DEBUG=False
   export SECRET_KEY='your-production-secret-key'
   export ALLOWED_HOSTS='yourdomain.com'
   ```

2. **Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Database**:
   - Consider using PostgreSQL for production
   - Run migrations: `python manage.py migrate`

4. **Web Server**:
   - Use Gunicorn or uWSGI
   - Configure behind Nginx or Apache

### Docker Deployment

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Error**:
   - Ensure `word_embeddings_smaller.pickle` exists in the `polls` directory
   - Check file permissions

2. **NLTK Data Missing**:
   ```bash
   python -c "import nltk; nltk.download('stopwords')"
   ```

3. **Port Already in Use**:
   ```bash
   python manage.py runserver 8001
   ```

4. **Template Filter Error**:
   - Restart the Django server after adding templatetags
   - Ensure `templatetags` directory is in the app directory

### Debug Mode

Enable debug mode for detailed error messages:
```python
# In mysite/settings.py
DEBUG = True
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the Django documentation for general questions

## 🔄 Version History

- **v2.0.0**: Complete rewrite with modern UI, improved error handling, and production-ready features
- **v1.0.0**: Initial basic implementation

---

**Note**: This application uses a pre-trained word embedding model. For production use, consider implementing your own word embeddings or using more advanced models like BERT for better accuracy.
