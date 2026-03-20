# Music Popularity Prediction

A machine learning project that predicts whether a song will become popular based on various audio features and artist characteristics.

## 🎵 Project Overview

This project uses a Neural Network (MLPClassifier) to predict song popularity using features extracted from music data. The model is trained on a dataset of 10,001 songs with 23 different features including audio characteristics, artist metrics, and temporal information.

## 📊 Dataset

The dataset contains the following key features:
- **Artist Features**: `artist_familiarity`, `artist_hotttnesss`, `artist_name`
- **Audio Features**: `duration`, `loudness`, `tempo`, `key`, `mode`, `time_signature`
- **Song Features**: `song_hotttnesss`, `start_of_fade_out`, `end_of_fade_in`
- **Temporal Features**: `year`, `release`
- **Target Variable**: `bbhot` (1 if song made it to Billboard Hot 100, 0 otherwise)

## 🛠️ Technologies Used

### Machine Learning Stack
- **Python 3.x**
- **scikit-learn 0.24.2** - Machine learning algorithms
- **pandas 1.1.5** - Data manipulation and analysis
- **numpy 1.21.5** - Numerical computing
- **matplotlib & seaborn** - Data visualization

### Web Application
- **Django 3.2** - Web framework
- **SQLite** - Database
- **HTML/CSS** - Frontend
- **pickle** - Model serialization

## 📁 Project Structure

```
music_popularity_prediction/
├── Dataset/
│   └── MusicDataset.csv          # Main dataset (10,001 songs)
├── Code/
│   ├── Song_popularity_prediction.ipynb  # Jupyter notebook for training
│   ├── train_model.py            # Python script for model training
│   └── mysite/                   # Django web application
│       ├── manage.py
│       ├── requirements.txt
│       ├── mysite/
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── .env
│       └── polls/
│           ├── views.py
│           ├── sustain.py
│           ├── models.py
│           ├── templates/
│           │   └── index.html
│           └── music-popularity-model.pkl
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd music_popularity_prediction
   ```

2. **Install dependencies**
   ```bash
   cd Code/mysite
   pip install -r requirements.txt
   ```

3. **Train the model** (if not already trained)
   ```bash
   cd Code
   python train_model.py
   ```
   This will create the trained model file at `mysite/polls/music-popularity-model.pkl`

### Running the Web Application

1. **Navigate to the Django project directory**
   ```bash
   cd Code/mysite
   ```

2. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

3. **Start the development server**
   ```bash
   python manage.py runserver
   ```

4. **Access the application**
   Open your web browser and go to `http://127.0.0.1:8000/`

## 🎯 Model Performance

The MLPClassifier achieved the following performance metrics:
- **Training Accuracy**: 87.91%
- **Test Accuracy**: 88.47%
- **Architecture**: 3 hidden layers (200, 150, 50 neurons)
- **Activation**: ReLU
- **Optimizer**: Adam
- **Max Iterations**: 200

## 📝 Feature Engineering

### Data Preprocessing Steps:
1. **Removed irrelevant features**: `artist_location`, `artist_latitude`, `artist_longitude`, `artist_name`, `release`, `title`
2. **Handled missing values**:
   - `song_hotttnesss`: Filled with mean
   - `artist_familiarity`: Filled with median
3. **Feature selection**: Dropped `end_of_fade_in`, `key`, `key_confidence`, `mode`, `mode_confidence`, `year`
4. **Final features**: 9 audio and artist metrics used for prediction

## 🌐 Web Interface

The web application provides:
- **User-friendly form** to input song features
- **Real-time predictions** using the trained model
- **Responsive design** with modern UI
- **Input validation** with appropriate field types

### Input Fields:
- Artist Familiarity (0-1)
- Artist Hotness (0-1)
- Duration (seconds)
- Loudness (dB)
- Song Hotness (0-1)
- Start of Fade Out (seconds)
- Tempo (BPM)
- Time Signature
- Time Signature Confidence (0-1)

## 🔧 Model Details

### Algorithm: Multilayer Perceptron (MLP)
- **Hidden Layers**: (200, 150, 50)
- **Activation Function**: ReLU
- **Solver**: Adam optimizer
- **Random State**: 1 (for reproducibility)
- **Maximum Iterations**: 200

### Class Distribution:
- **Non-popular songs** (bbhot=0): 8,809 (88.08%)
- **Popular songs** (bbhot=1): 1,192 (11.92%)

## 📈 Usage Examples

### Using the Web Interface:
1. Open `http://127.0.0.1:8000/` in your browser
2. Fill in the song feature values
3. Click "Predict" to get the popularity prediction
4. View the result with emoji indicators

### Using the Model Directly:
```python
import pickle
import pandas as pd

# Load the trained model
model = pickle.load(open('mysite/polls/music-popularity-model.pkl', 'rb'))

# Create sample data
sample_data = pd.DataFrame({
    'artist_familiarity': [0.7],
    'artist_hotttnesss': [0.5],
    'duration': [240.0],
    'loudness': [-5.0],
    'song_hotttnesss': [0.6],
    'start_of_fade_out': [230.0],
    'tempo': [120.0],
    'time_signature': [4],
    'time_signature_confidence': [0.9]
})

# Make prediction
prediction = model.predict(sample_data)
print(f"Prediction: {'Popular' if prediction[0] == 1 else 'Not Popular'}")
```

## 🐛 Known Issues

- The model shows bias towards predicting non-popular songs due to class imbalance
- Some features like `song_hotttnesss` may not be available for new/unreleased songs
- The model performance could be improved with more balanced dataset or different algorithms

## 🔮 Future Improvements

1. **Address class imbalance** using techniques like SMOTE or class weights
2. **Feature engineering** to create more meaningful features
3. **Model optimization** with hyperparameter tuning
4. **Additional algorithms** like Random Forest, XGBoost, or deep learning
5. **Cross-validation** for more robust performance evaluation
6. **API endpoint** for programmatic access
7. **Batch prediction** functionality
8. **Model interpretability** using SHAP or LIME

## 📄 License

This project is for educational purposes. Please refer to the dataset license for usage restrictions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Contact

For questions or suggestions about this project, please open an issue in the repository.

---

**Note**: This project was developed as part of machine learning education and demonstrates the complete pipeline from data preprocessing to web deployment.
