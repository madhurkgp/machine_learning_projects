# IMDB Movie Rating Predictor

A production-ready Django web application that predicts IMDB movie ratings using machine learning algorithms. This application uses a Random Forest model trained on comprehensive movie metadata to provide accurate rating predictions with confidence scores.

## Features

- **Modern Web Interface**: Responsive, mobile-friendly design with smooth animations and gradients
- **ML-Powered Predictions**: Random Forest model with 18 features including financial, social media, and review metrics
- **Confidence Scores**: Each prediction includes a confidence percentage
- **Rating Categorization**: Predictions are categorized as Excellent, Good, Average, Below Average, or Poor
- **Sample Data**: Built-in sample movie data for easy testing
- **Form Validation**: Comprehensive input validation with user-friendly error messages
- **Production Ready**: Optimized for deployment with proper error handling and logging

## Technology Stack

- **Backend**: Django 4.2.7
- **Machine Learning**: scikit-learn 1.3.2
- **Data Processing**: pandas 2.1.3, numpy 1.24.3
- **Model Persistence**: joblib 1.3.2
- **Frontend**: Bootstrap 5, Font Awesome 6
- **Deployment**: gunicorn, whitenoise

## Model Details

### Algorithm
- **Random Forest Regressor**
- **100 estimators**
- **Max depth: 10**
- **Random state: 42**

### Performance Metrics
- **Mean Squared Error**: 0.7680
- **R² Score**: 0.4394

### Features Used (18 total)
1. **Basic Information**
   - Duration (minutes)
   - Release Year
   - Color (Color/Black & White)
   - Content Rating
   - Language
   - Country

2. **Financial Data**
   - Budget (USD)
   - Gross Revenue (USD)

3. **Social Media Metrics**
   - Director Facebook Likes
   - Main Actor Facebook Likes
   - Second Actor Facebook Likes
   - Third Actor Facebook Likes
   - Movie Facebook Likes
   - Total Cast Facebook Likes

4. **Reviews & Ratings**
   - Number of Critic Reviews
   - Number of User Reviews
   - Number of Voted Users

5. **Visual & Cast**
   - Number of Faces in Poster
   - Aspect Ratio

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd imbd-prediction
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix/MacOS
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Train the ML Model
```bash
python prediction/ml_model.py
```
This will:
- Load and preprocess the movie metadata dataset
- Train the Random Forest model
- Save the model artifacts to `static/models/`

### Step 5: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 7: Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Usage Guide

### Making Predictions

1. **Fill the Form**: Enter movie details in the comprehensive form
2. **Use Sample Data**: Click "Load Sample Data" to test with pre-filled values
3. **Submit**: Click "Predict Rating" to get the prediction
4. **View Results**: See the predicted rating, category, and confidence score

### Rating Categories
- **Excellent** (8.0+): Outstanding movies with high ratings
- **Good** (7.0-7.9): Well-received movies
- **Average** (6.0-6.9): Decent movies
- **Below Average** (5.0-5.9): Mediocre movies
- **Poor** (below 5.0): Poorly rated movies

### Confidence Scores
Confidence scores range from 0-100% and indicate the model's certainty in its prediction. Higher confidence means the prediction is more reliable.

## API Documentation

### POST /predict/
Predicts IMDB rating for a movie.

**Request**: Form data with the following fields:
- `num_critic_for_reviews`: Number of critic reviews (1-1000)
- `duration`: Duration in minutes (1-500)
- `director_facebook_likes`: Director's Facebook likes (0-100000)
- `actor_3_facebook_likes`: Third actor's Facebook likes (0-100000)
- `actor_1_facebook_likes`: Main actor's Facebook likes (0-1000000)
- `gross`: Gross revenue in USD (0+)
- `num_voted_users`: Number of voted users (0-2000000)
- `cast_total_facebook_likes`: Total cast Facebook likes (0-1000000)
- `facenumber_in_poster`: Number of faces in poster (0-50)
- `num_user_for_reviews`: Number of user reviews (0-10000)
- `budget`: Movie budget in USD (0+)
- `title_year`: Release year (1900-2030)
- `actor_2_facebook_likes`: Second actor's Facebook likes (0-200000)
- `aspect_ratio`: Aspect ratio (0.5-5.0)
- `movie_facebook_likes`: Movie's Facebook likes (0-500000)
- `color`: Color type ('Color' or ' Black and White')
- `content_rating`: Content rating ('G', 'PG', 'PG-13', 'R', etc.)
- `language`: Movie language ('English', 'French', etc.)
- `country`: Production country ('USA', 'UK', etc.)

**Response** (JSON):
```json
{
    "success": true,
    "predicted_rating": 7.8,
    "confidence": 85.2,
    "category": "Good",
    "color_class": "good"
}
```

### GET /sample-data/
Returns sample movie data for testing.

**Response** (JSON):
```json
{
    "samples": [
        {
            "name": "Avatar",
            "data": { ... }
        }
    ]
}
```

## Project Structure

```
imbd-prediction/
|
|-- imdb_project/           # Main Django project
|   |-- settings.py         # Django settings
|   |-- urls.py            # Main URL configuration
|   |-- wsgi.py            # WSGI configuration
|
|-- prediction/            # Prediction app
|   |-- views.py           # Main views
|   |-- forms.py           # Django forms
|   |-- ml_model.py        # ML model and prediction logic
|   |-- urls.py            # App URL configuration
|   |-- templates/
|   |   |-- prediction/
|   |       |-- home.html  # Main template
|
|-- static/
|   |-- models/            # Trained ML models
|   |   |-- imdb_model.pkl
|   |   |-- label_encoders.pkl
|   |   |-- feature_columns.pkl
|
|-- Notebook/              # Original Jupyter notebook
|   |-- IMDB Movie Ratings Prediction.ipynb
|   |-- movie_metadata.csv
|
|-- requirements.txt       # Python dependencies
|-- manage.py             # Django management script
|-- README.md             # This file
```

## Model Training Process

1. **Data Loading**: Load movie metadata from CSV
2. **Feature Selection**: Select 18 relevant features
3. **Preprocessing**:
   - Handle missing values (median for numeric, mode for categorical)
   - Encode categorical variables using LabelEncoder
4. **Training**: Split data (80/20) and train Random Forest
5. **Evaluation**: Calculate MSE and R² score
6. **Persistence**: Save model, encoders, and feature list

## Deployment

### Production Deployment

1. **Environment Variables**:
   - Set `DEBUG=False`
   - Configure `ALLOWED_HOSTS`
   - Set `SECRET_KEY`

2. **Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Using Gunicorn**:
   ```bash
   gunicorn imdb_project.wsgi:application
   ```

4. **Using Whitenoise** (already configured):
   - Static files are served efficiently
   - No additional web server needed for static content

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python prediction/ml_model.py
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "imdb_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Troubleshooting

### Common Issues

1. **Model Not Found Error**:
   - Run `python prediction/ml_model.py` to train and save the model
   - Ensure `static/models/` directory exists and contains model files

2. **Import Errors**:
   - Check all dependencies are installed: `pip install -r requirements.txt`
   - Verify Python version compatibility (3.8+)

3. **Database Issues**:
   - Run migrations: `python manage.py migrate`
   - Delete `db.sqlite3` and re-migrate if needed

4. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATICFILES_DIRS` settings

5. **Prediction Errors**:
   - Ensure all form fields are filled with valid data
   - Check that model files are not corrupted

### Performance Optimization

1. **Model Loading**: Model is loaded once at startup for efficiency
2. **Caching**: Consider Redis caching for frequent predictions
3. **Database**: Use PostgreSQL for production instead of SQLite
4. **Static Files**: Use CDN for static file serving in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and demonstration purposes. Please ensure compliance with the original dataset's terms of use.

## Acknowledgments

- Dataset: IMDB Movie Metadata
- ML Framework: scikit-learn
- Web Framework: Django
- UI Framework: Bootstrap

## Future Enhancements

- [ ] Add more ML algorithms (XGBoost, Neural Networks)
- [ ] Implement model versioning
- [ ] Add user authentication and prediction history
- [ ] Include movie poster upload and analysis
- [ ] Add API rate limiting
- [ ] Implement A/B testing for different models
- [ ] Add movie recommendation features
- [ ] Include real-time social media sentiment analysis
