import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib


class RestaurantRatingPredictor:
    """Machine Learning model for restaurant rating prediction"""
    
    def __init__(self):
        self.models = {}
        self.encoders = {}
        self.feature_columns = []
        self.target_column = 'rate'
        self.model_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
        
        # Create model directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Initialize models
        self._initialize_models()
        
        # Try to load pre-trained models
        self._load_models()
    
    def _initialize_models(self):
        """Initialize ML models"""
        self.models = {
            'RandomForest': RandomForestRegressor(
                n_estimators=100,
                criterion='squared_error',
                max_depth=None,
                min_samples_split=2,
                min_samples_leaf=1,
                random_state=42
            ),
            'LinearRegression': LinearRegression(),
            'DecisionTree': DecisionTreeRegressor(
                criterion='squared_error',
                max_depth=None,
                min_samples_split=2,
                min_samples_leaf=1,
                random_state=42
            )
        }
    
    def _load_models(self):
        """Load pre-trained models if available"""
        try:
            for model_name in self.models.keys():
                model_path = os.path.join(self.model_dir, f'{model_name.lower()}_model.pkl')
                encoder_path = os.path.join(self.model_dir, f'{model_name.lower()}_encoder.pkl')
                
                if os.path.exists(model_path) and os.path.exists(encoder_path):
                    self.models[model_name] = joblib.load(model_path)
                    self.encoders[model_name] = joblib.load(encoder_path)
        except Exception as e:
            print(f"Warning: Could not load pre-trained models: {e}")
    
    def _preprocess_input(self, data):
        """Preprocess input data for prediction"""
        # Convert input to DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = data.copy()
        
        # Ensure boolean columns are properly formatted
        df['online_order'] = df['online_order'].astype(bool)
        df['book_table'] = df['book_table'].astype(bool)
        
        # Convert cost to numeric
        if 'approx_cost' in df.columns:
            df['approx_cost'] = pd.to_numeric(df['approx_cost'], errors='coerce')
        
        return df
    
    def _encode_features(self, df, model_name='RandomForest'):
        """Encode categorical features"""
        encoded_df = df.copy()
        
        # Get or create encoder for the model
        if model_name not in self.encoders:
            self.encoders[model_name] = {}
        
        # Encode categorical columns
        categorical_columns = ['location', 'rest_type', 'cuisines']
        
        for col in categorical_columns:
            if col in encoded_df.columns:
                if col not in self.encoders[model_name]:
                    # Create new encoder
                    self.encoders[model_name][col] = LabelEncoder()
                    # Fit with common values (fallback)
                    common_values = self._get_common_values_for_column(col)
                    self.encoders[model_name][col].fit(common_values)
                
                # Handle unseen values
                unique_values = encoded_df[col].unique()
                encoder_values = self.encoders[model_name][col].classes_
                
                # Map unseen values to a default value
                for val in unique_values:
                    if val not in encoder_values:
                        encoded_df.loc[encoded_df[col] == val, col] = encoder_values[0]
                
                # Transform the column
                encoded_df[col] = self.encoders[model_name][col].transform(encoded_df[col])
        
        return encoded_df
    
    def _get_common_values_for_column(self, column):
        """Get common values for a column based on typical Bangalore restaurants"""
        common_values = {
            'location': ['BTM', 'Banashankari', 'Basavanagudi', 'Jayanagar', 'Koramangala', 
                       'Indiranagar', 'Electronic City', 'Marathahalli', 'Whitefield', 'HSR Layout'],
            'rest_type': ['Casual Dining', 'Quick Bites', 'Cafe', 'Delivery', 'Dessert Parlor',
                         'Bakery', 'Fine Dining', 'Bar', 'Pub', 'Lounge', 'Food Court'],
            'cuisines': ['North Indian', 'South Indian', 'Chinese', 'Italian', 'Continental',
                        'Mexican', 'Thai', 'Japanese', 'Arabian', 'Mughlai', 'Biryani',
                        'Fast Food', 'Cafe', 'Desserts', 'Beverages']
        }
        return common_values.get(column, ['Other'])
    
    def _prepare_features(self, df):
        """Prepare feature columns for prediction"""
        # Define feature columns
        self.feature_columns = [
            'online_order', 'book_table', 'votes', 'location', 
            'rest_type', 'cuisines', 'approx_cost'
        ]
        
        # Ensure all required columns exist
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0  # Default value
        
        # Select only feature columns
        features_df = df[self.feature_columns].copy()
        
        # Fill missing values
        features_df = features_df.fillna(0)
        
        return features_df
    
    def predict_rating(self, input_data, model_name='RandomForest'):
        """Make prediction using specified model"""
        try:
            # Preprocess input
            processed_data = self._preprocess_input(input_data)
            
            # Encode features
            encoded_data = self._encode_features(processed_data, model_name)
            
            # Prepare features
            features = self._prepare_features(encoded_data)
            
            # Make prediction
            if model_name in self.models:
                model = self.models[model_name]
                prediction = model.predict(features)[0]
                
                # Ensure prediction is within valid range
                prediction = max(1.0, min(5.0, prediction))
                
                # Calculate confidence score (simplified)
                confidence_score = self._calculate_confidence_score(model, features, prediction)
                
                return {
                    'predicted_rating': round(float(prediction), 2),
                    'model_used': model_name,
                    'confidence_score': round(float(confidence_score), 3),
                    'features_used': self.feature_columns
                }
            else:
                raise ValueError(f"Model '{model_name}' not available")
                
        except Exception as e:
            # Fallback to simple rule-based prediction
            return self._fallback_prediction(input_data)
    
    def _calculate_confidence_score(self, model, features, prediction):
        """Calculate confidence score for prediction"""
        try:
            # Simple confidence calculation based on feature values
            # This is a simplified version - in production, you'd use more sophisticated methods
            
            votes = features['votes'].iloc[0] if 'votes' in features.columns else 0
            cost = features['approx_cost'].iloc[0] if 'approx_cost' in features.columns else 0
            
            # Higher confidence for restaurants with more votes and reasonable cost
            vote_confidence = min(1.0, votes / 1000)  # Normalize votes
            cost_confidence = 1.0 if 100 <= cost <= 1000 else 0.7
            
            # Overall confidence (simplified)
            confidence = (vote_confidence + cost_confidence) / 2
            
            return max(0.1, min(1.0, confidence))
        except:
            return 0.5  # Default confidence
    
    def _fallback_prediction(self, input_data):
        """Fallback prediction using simple rules"""
        try:
            # Simple rule-based prediction
            base_rating = 3.0
            
            # Adjust based on features
            if input_data.get('online_order', False):
                base_rating += 0.2
            
            if input_data.get('book_table', False):
                base_rating += 0.3
            
            votes = input_data.get('votes', 0)
            if votes > 100:
                base_rating += 0.3
            elif votes > 50:
                base_rating += 0.1
            
            cost = input_data.get('approx_cost', 0)
            if cost > 1000:
                base_rating += 0.2
            elif cost < 200:
                base_rating -= 0.1
            
            # Ensure within bounds
            base_rating = max(1.0, min(5.0, base_rating))
            
            return {
                'predicted_rating': round(float(base_rating), 2),
                'model_used': 'RuleBased',
                'confidence_score': 0.5,
                'features_used': list(input_data.keys())
            }
        except:
            return {
                'predicted_rating': 3.5,
                'model_used': 'Default',
                'confidence_score': 0.3,
                'features_used': []
            }
    
    def train_models(self, data_path=None):
        """Train models with sample data (for demonstration)"""
        try:
            # Generate sample data if no data path provided
            if data_path is None:
                df = self._generate_sample_data()
            else:
                df = pd.read_csv(data_path)
            
            # Preprocess data
            df = self._preprocess_training_data(df)
            
            # Prepare features and target
            X = df.drop(self.target_column, axis=1)
            y = df[self.target_column]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train each model
            results = {}
            for model_name, model in self.models.items():
                # Train model
                model.fit(X_train, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                r2 = r2_score(y_test, y_pred)
                mse = mean_squared_error(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                
                results[model_name] = {
                    'r2_score': r2,
                    'mse': mse,
                    'mae': mae
                }
                
                # Save model and encoder
                model_path = os.path.join(self.model_dir, f'{model_name.lower()}_model.pkl')
                encoder_path = os.path.join(self.model_dir, f'{model_name.lower()}_encoder.pkl')
                
                joblib.dump(model, model_path)
                joblib.dump(self.encoders.get(model_name, {}), encoder_path)
            
            return results
            
        except Exception as e:
            print(f"Error training models: {e}")
            return {}
    
    def _preprocess_training_data(self, df):
        """Preprocess training data"""
        # This would contain the actual preprocessing from the notebook
        # For now, return a basic processed dataframe
        return df
    
    def _generate_sample_data(self):
        """Generate sample training data"""
        # Generate sample data for demonstration
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'online_order': np.random.choice([True, False], n_samples),
            'book_table': np.random.choice([True, False], n_samples),
            'votes': np.random.randint(0, 5000, n_samples),
            'location': np.random.choice(['BTM', 'Koramangala', 'Indiranagar', 'Jayanagar'], n_samples),
            'rest_type': np.random.choice(['Casual Dining', 'Quick Bites', 'Cafe'], n_samples),
            'cuisines': np.random.choice(['North Indian', 'Chinese', 'Italian'], n_samples),
            'approx_cost': np.random.randint(100, 2000, n_samples),
            'rate': np.random.uniform(2.0, 5.0, n_samples)
        }
        
        return pd.DataFrame(data)
