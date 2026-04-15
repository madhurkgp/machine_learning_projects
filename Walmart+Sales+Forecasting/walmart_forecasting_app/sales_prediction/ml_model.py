import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class WalmartSalesPredictor:
    def __init__(self):
        self.ridge_model = None
        self.lasso_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def load_and_train_models(self, data_path=None):
        """Load data and train Ridge and Lasso models"""
        try:
            # If data_path is provided, load from there, otherwise use sample data
            if data_path and os.path.exists(data_path):
                train_df = pd.read_csv(os.path.join(data_path, 'train.csv'))
                features_df = pd.read_csv(os.path.join(data_path, 'features.csv'))
                stores_df = pd.read_csv(os.path.join(data_path, 'stores.csv'))
            else:
                # Create sample data for demonstration
                train_df = self._create_sample_data()
                features_df = self._create_sample_features()
                stores_df = self._create_sample_stores()
            
            # Data preprocessing
            dataset = features_df.merge(stores_df, how='inner', on='Store')
            dataset['Date'] = pd.to_datetime(dataset['Date'])
            dataset['Week'] = dataset.Date.dt.isocalendar().week
            dataset['Year'] = dataset.Date.dt.year
            
            train_df['Date'] = pd.to_datetime(train_df['Date'])
            train_merge = train_df.merge(dataset, how='inner', on=['Store', 'Date', 'IsHoliday'])
            
            # Select features based on correlation analysis from notebook
            features = ['Store', 'Dept', 'IsHoliday', 'Size', 'Week', 'Year']
            X = train_merge[features]
            y = train_merge['Weekly_Sales']
            
            # Handle categorical variables
            X = pd.get_dummies(X, columns=['IsHoliday'], drop_first=True)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train Ridge model
            self.ridge_model = Ridge(alpha=1.0)
            self.ridge_model.fit(X_train_scaled, y_train)
            
            # Train Lasso model
            self.lasso_model = Lasso(alpha=1.0)
            self.lasso_model.fit(X_train_scaled, y_train)
            
            self.is_trained = True
            self.feature_names = X.columns.tolist()
            
            return True
            
        except Exception as e:
            print(f"Error training models: {e}")
            return False
    
    def predict(self, store, department, is_holiday, temperature, cpi, unemployment, size, week, year):
        """Make prediction using trained models"""
        if not self.is_trained:
            return None, None, "Models not trained yet"
        
        try:
            # Create input dataframe
            input_data = pd.DataFrame({
                'Store': [store],
                'Dept': [department],
                'IsHoliday': [is_holiday],
                'Size': [size],
                'Week': [week],
                'Year': [year]
            })
            
            # Handle categorical variables
            input_data = pd.get_dummies(input_data, columns=['IsHoliday'], drop_first=True)
            
            # Ensure all required columns are present
            for col in self.feature_names:
                if col not in input_data.columns:
                    input_data[col] = 0
            
            # Reorder columns to match training data
            input_data = input_data[self.feature_names]
            
            # Scale features
            input_scaled = self.scaler.transform(input_data)
            
            # Make predictions
            ridge_pred = self.ridge_model.predict(input_scaled)[0]
            lasso_pred = self.lasso_model.predict(input_scaled)[0]
            
            # Use Ridge as primary and Lasso as secondary
            final_prediction = ridge_pred
            
            # Calculate confidence score based on model agreement
            confidence = 1.0 - abs(ridge_pred - lasso_pred) / max(abs(ridge_pred), abs(lasso_pred), 1)
            confidence = max(0, min(1, confidence))  # Clamp between 0 and 1
            
            return final_prediction, confidence, None
            
        except Exception as e:
            return None, None, f"Prediction error: {str(e)}"
    
    def _create_sample_data(self):
        """Create sample training data"""
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'Store': np.random.randint(1, 46, n_samples),
            'Dept': np.random.randint(1, 100, n_samples),
            'Date': pd.date_range('2010-01-01', periods=n_samples, freq='W'),
            'Weekly_Sales': np.random.normal(15000, 8000, n_samples),
            'IsHoliday': np.random.choice([True, False], n_samples, p=[0.07, 0.93])
        }
        
        return pd.DataFrame(data)
    
    def _create_sample_features(self):
        """Create sample features data"""
        np.random.seed(42)
        n_samples = 500
        
        data = {
            'Store': np.random.randint(1, 46, n_samples),
            'Date': pd.date_range('2010-01-01', periods=n_samples, freq='W'),
            'Temperature': np.random.normal(60, 20, n_samples),
            'Fuel_Price': np.random.normal(3.0, 0.5, n_samples),
            'MarkDown1': np.random.normal(5000, 2000, n_samples),
            'MarkDown2': np.random.normal(3000, 1500, n_samples),
            'MarkDown3': np.random.normal(2000, 1000, n_samples),
            'MarkDown4': np.random.normal(4000, 1800, n_samples),
            'MarkDown5': np.random.normal(3500, 1600, n_samples),
            'CPI': np.random.normal(170, 40, n_samples),
            'Unemployment': np.random.normal(7.5, 2.0, n_samples),
            'IsHoliday': np.random.choice([True, False], n_samples, p=[0.07, 0.93])
        }
        
        return pd.DataFrame(data)
    
    def _create_sample_stores(self):
        """Create sample stores data"""
        stores = []
        for i in range(1, 46):
            store_type = np.random.choice(['A', 'B', 'C'], p=[0.5, 0.35, 0.15])
            if store_type == 'A':
                size = np.random.randint(150000, 220000)
            elif store_type == 'B':
                size = np.random.randint(70000, 150000)
            else:
                size = np.random.randint(30000, 70000)
            
            stores.append({
                'Store': i,
                'Type': store_type,
                'Size': size
            })
        
        return pd.DataFrame(stores)

# Global predictor instance
predictor = WalmartSalesPredictor()
