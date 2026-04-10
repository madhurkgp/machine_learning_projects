import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime, timedelta
import requests

class CovidPredictor:
    """ML model for COVID-19 case prediction"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'active_cases', 'positive_cases', 'cured_cases', 'death_cases',
            'new_active', 'new_positive', 'new_cured', 'new_death'
        ]
        self.model_path = os.path.join(os.path.dirname(__file__), 'covid_model.pkl')
        self.scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
        
    def load_sample_data(self):
        """Load sample COVID-19 data for training"""
        # Sample data based on typical COVID-19 patterns
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'active_cases': np.random.randint(100, 50000, n_samples),
            'positive_cases': np.random.randint(1000, 100000, n_samples),
            'cured_cases': np.random.randint(800, 90000, n_samples),
            'death_cases': np.random.randint(10, 2000, n_samples),
            'new_active': np.random.randint(5, 500, n_samples),
            'new_positive': np.random.randint(50, 2000, n_samples),
            'new_cured': np.random.randint(40, 1800, n_samples),
            'new_death': np.random.randint(1, 50, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Create target variables (next day predictions)
        df['target_active'] = df['active_cases'] + np.random.randint(-100, 100, n_samples)
        df['target_positive'] = df['positive_cases'] + np.random.randint(-50, 500, n_samples)
        df['target_cured'] = df['cured_cases'] + np.random.randint(-30, 300, n_samples)
        df['target_death'] = df['death_cases'] + np.random.randint(0, 20, n_samples)
        
        return df
    
    def train_model(self):
        """Train the ML model"""
        print("Training COVID-19 prediction model...")
        
        # Load sample data
        df = self.load_sample_data()
        
        # Prepare features and targets
        X = df[self.feature_columns]
        y_active = df['target_active']
        y_positive = df['target_positive']
        y_cured = df['target_cured']
        y_death = df['target_death']
        
        # Split data
        X_train, X_test, y_active_train, y_active_test = train_test_split(
            X, y_active, test_size=0.2, random_state=42
        )
        _, _, y_positive_train, y_positive_test = train_test_split(
            X, y_positive, test_size=0.2, random_state=42
        )
        _, _, y_cured_train, y_cured_test = train_test_split(
            X, y_cured, test_size=0.2, random_state=42
        )
        _, _, y_death_train, y_death_test = train_test_split(
            X, y_death, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train models for each target
        models = {}
        targets = {
            'active': (y_active_train, y_active_test),
            'positive': (y_positive_train, y_positive_test),
            'cured': (y_cured_train, y_cured_test),
            'death': (y_death_train, y_death_test)
        }
        
        for target_name, (y_train, y_test) in targets.items():
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            print(f"{target_name.title()} Model - MAE: {mae:.2f}, MSE: {mse:.2f}, R2: {r2:.3f}")
            models[target_name] = model
        
        self.model = models
        
        # Save models and scaler
        joblib.dump(models, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        print("Model training completed and saved!")
        return True
    
    def load_model(self):
        """Load pre-trained model"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                print("Model loaded successfully!")
                return True
            else:
                print("No pre-trained model found. Training new model...")
                return self.train_model()
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Training new model...")
            return self.train_model()
    
    def predict(self, input_data):
        """Make predictions for COVID-19 cases"""
        if self.model is None:
            self.load_model()
        
        try:
            # Prepare input data
            if isinstance(input_data, dict):
                df = pd.DataFrame([input_data])
            else:
                df = input_data
            
            # Ensure all required columns are present
            for col in self.feature_columns:
                if col not in df.columns:
                    df[col] = 0
            
            # Scale features
            X_scaled = self.scaler.transform(df[self.feature_columns])
            
            # Make predictions
            predictions = {}
            for target_name, model in self.model.items():
                pred = model.predict(X_scaled)[0]
                predictions[f'predicted_{target_name}'] = max(0, int(pred))  # Ensure non-negative
            
            # Calculate confidence score (simplified)
            confidence = np.random.uniform(0.75, 0.95)  # Simulated confidence
            
            return {
                **predictions,
                'confidence_score': confidence,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'predicted_active': 0,
                'predicted_positive': 0,
                'predicted_cured': 0,
                'predicted_death': 0,
                'confidence_score': 0.0
            }
    
    def get_feature_importance(self):
        """Get feature importance from the model"""
        if self.model is None:
            self.load_model()
        
        # Use active model as reference for feature importance
        active_model = self.model.get('active')
        if active_model:
            importance = active_model.feature_importances_
            feature_importance = dict(zip(self.feature_columns, importance))
            return dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
        return {}
    
    def validate_input(self, data):
        """Validate input data"""
        required_fields = self.feature_columns
        errors = []
        
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(data[field], (int, float)) or data[field] < 0:
                errors.append(f"Field {field} must be a non-negative number")
        
        return len(errors) == 0, errors

# Global predictor instance
predictor = CovidPredictor()
