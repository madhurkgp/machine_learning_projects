import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class IMDBRatingPredictor:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_columns = []
        self.model_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'models')
        
    def load_and_preprocess_data(self, csv_path):
        """Load and preprocess the movie metadata dataset"""
        df = pd.read_csv(csv_path)
        
        # Select relevant features for prediction
        features = [
            'num_critic_for_reviews', 'duration', 'director_facebook_likes',
            'actor_3_facebook_likes', 'actor_1_facebook_likes', 'gross',
            'num_voted_users', 'cast_total_facebook_likes', 'facenumber_in_poster',
            'num_user_for_reviews', 'budget', 'title_year', 'actor_2_facebook_likes',
            'aspect_ratio', 'movie_facebook_likes', 'color', 'content_rating',
            'language', 'country'
        ]
        
        # Keep only the features that exist in the dataset
        available_features = [f for f in features if f in df.columns]
        df = df[available_features + ['imdb_score']].copy()
        
        # Handle missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col] = df[col].fillna(df[col].median())
            
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')
        
        # Encode categorical variables
        for col in categorical_columns:
            if col != 'imdb_score':
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                self.label_encoders[col] = le
        
        # Store feature columns (excluding target)
        self.feature_columns = [col for col in df.columns if col != 'imdb_score']
        
        return df
    
    def train_model(self, df):
        """Train the Random Forest model"""
        X = df[self.feature_columns]
        y = df['imdb_score']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model trained successfully!")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"R² Score: {r2:.4f}")
        
        return mse, r2
    
    def save_model(self):
        """Save the trained model and encoders"""
        os.makedirs(self.model_path, exist_ok=True)
        
        joblib.dump(self.model, os.path.join(self.model_path, 'imdb_model.pkl'))
        joblib.dump(self.label_encoders, os.path.join(self.model_path, 'label_encoders.pkl'))
        joblib.dump(self.feature_columns, os.path.join(self.model_path, 'feature_columns.pkl'))
        
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load the trained model and encoders"""
        try:
            self.model = joblib.load(os.path.join(self.model_path, 'imdb_model.pkl'))
            self.label_encoders = joblib.load(os.path.join(self.model_path, 'label_encoders.pkl'))
            self.feature_columns = joblib.load(os.path.join(self.model_path, 'feature_columns.pkl'))
            print("Model loaded successfully!")
            return True
        except FileNotFoundError:
            print("Model files not found. Please train the model first.")
            return False
    
    def predict_rating(self, movie_data):
        """Predict IMDB rating for a new movie"""
        if self.model is None:
            if not self.load_model():
                return None, None
        
        # Convert input to DataFrame
        df = pd.DataFrame([movie_data])
        
        # Ensure all required features are present
        for feature in self.feature_columns:
            if feature not in df.columns:
                df[feature] = 0  # Default value for missing features
        
        # Encode categorical variables
        for col, encoder in self.label_encoders.items():
            if col in df.columns:
                try:
                    df[col] = encoder.transform(df[col])
                except ValueError:
                    # Handle unseen categories
                    df[col] = 0
        
        # Make prediction
        prediction = self.model.predict(df[self.feature_columns])[0]
        
        # Calculate confidence score based on prediction range
        confidence = max(0, min(100, 100 - abs(prediction - 6.5) * 10))
        
        return round(prediction, 1), round(confidence, 1)

def train_and_save_model():
    """Train and save the model using the dataset"""
    predictor = IMDBRatingPredictor()
    
    # Load and preprocess data
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'Notebook', 'movie_metadata.csv')
    df = predictor.load_and_preprocess_data(csv_path)
    
    # Train model
    mse, r2 = predictor.train_model(df)
    
    # Save model
    predictor.save_model()
    
    return predictor

if __name__ == "__main__":
    # Train the model when script is run directly
    predictor = train_and_save_model()
