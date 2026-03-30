import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler

class BlackFridayPredictor:
    def __init__(self):
        self.model = None
        self.feature_scaler = None
        self.product_id_scaler = None
        self.feature_columns = None
        self.preprocessing_info = None
        self.original_data_info = None
        self.label_encoders = {}
        
        # Load all saved objects
        self.load_models()
    
    def load_models(self):
        """Load all saved ML models and preprocessing objects"""
        try:
            # Get the base directory (project root)
            current_dir = os.path.dirname(os.path.dirname(__file__))
            models_dir = os.path.join(current_dir, 'models')
            
            # Load the trained model
            self.model = joblib.load(os.path.join(models_dir, 'random_forest_model.pkl'))
            
            # Load scalers
            self.feature_scaler = joblib.load(os.path.join(models_dir, 'feature_scaler.pkl'))
            self.product_id_scaler = joblib.load(os.path.join(models_dir, 'product_id_scaler.pkl'))
            
            # Load feature columns and preprocessing info
            self.feature_columns = joblib.load(os.path.join(models_dir, 'feature_columns.pkl'))
            self.preprocessing_info = joblib.load(os.path.join(models_dir, 'preprocessing_info.pkl'))
            self.original_data_info = joblib.load(os.path.join(models_dir, 'original_data_info.pkl'))
            
            # Initialize label encoders with original values
            self._initialize_label_encoders()
            
        except Exception as e:
            raise Exception(f"Error loading ML models: {str(e)}")
    
    def _initialize_label_encoders(self):
        """Initialize label encoders with original categorical values"""
        # Gender encoder
        gender_le = LabelEncoder()
        gender_le.fit(self.original_data_info['gender_values'])
        self.label_encoders['Gender'] = gender_le
        
        # Age encoder
        age_le = LabelEncoder()
        age_le.fit(self.original_data_info['age_values'])
        self.label_encoders['Age'] = age_le
        
        # City Category encoder
        city_le = LabelEncoder()
        city_le.fit(self.original_data_info['city_category_values'])
        self.label_encoders['City_Category'] = city_le
    
    def preprocess_input(self, form_data):
        """Preprocess input data to match the model's expected format"""
        try:
            # Create a dictionary with the input data
            data = {
                'User_ID': [int(form_data.get('user_id', 1000001))],
                'Product_ID': [form_data.get('product_id', 'P00069042')],
                'Gender': [form_data.get('gender', 'M')],
                'Age': [form_data.get('age', '26-35')],
                'Occupation': [int(form_data.get('occupation', 0))],
                'City_Category': [form_data.get('city_category', 'A')],
                'Stay_In_Current_City_Years': [form_data.get('stay_years', '2')],
                'Marital_Status': [int(form_data.get('marital_status', 0))],
                'Product_Category_1': [int(form_data.get('product_category_1', 1))],
                'Product_Category_2': [float(form_data.get('product_category_2', self.preprocessing_info['product_category_2_mean']))]
            }
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Process Product_ID
            df['Product_ID'] = df['Product_ID'].str.replace('P00', '')
            df['Product_ID'] = self.product_id_scaler.transform(df['Product_ID'].values.reshape(-1, 1))
            
            # Handle missing Product_Category_2
            if df['Product_Category_2'].isna().any():
                df['Product_Category_2'] = df['Product_Category_2'].fillna(self.preprocessing_info['product_category_2_mean'])
            
            # Apply label encoding to categorical variables
            for col in ['Gender', 'City_Category', 'Age']:
                if col in df.columns:
                    df[col] = self.label_encoders[col].transform(df[col])
            
            # Handle Stay_In_Current_City_Years
            df['Stay_In_Current_City_Years'] = df['Stay_In_Current_City_Years'].replace('4+', '4')
            df['Stay_In_Current_City_Years'] = df['Stay_In_Current_City_Years'].astype(int)
            
            # Convert categorical columns to proper types
            df['Gender'] = df['Gender'].astype(int)
            df['Age'] = df['Age'].astype(int)
            df['City_Category'] = df['City_Category'].astype('category')
            
            # Create dummy variables
            df = pd.get_dummies(df)
            
            # Ensure all expected columns are present (fill missing with 0)
            for col in self.feature_columns:
                if col not in df.columns:
                    df[col] = 0
            
            # Reorder columns to match training data
            df = df[self.feature_columns]
            
            return df
            
        except Exception as e:
            raise Exception(f"Error preprocessing input data: {str(e)}")
    
    def predict(self, form_data):
        """Make prediction on input data"""
        try:
            # Preprocess input
            processed_data = self.preprocess_input(form_data)
            
            # Scale features
            scaled_data = self.feature_scaler.transform(processed_data)
            
            # Make prediction
            prediction_log = self.model.predict(scaled_data)[0]
            
            # Convert back from log scale
            prediction = np.exp(prediction_log)
            
            # Round to nearest integer
            prediction = round(prediction)
            
            return prediction
            
        except Exception as e:
            raise Exception(f"Error making prediction: {str(e)}")
    
    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if hasattr(self.model, 'feature_importances_'):
            importance_dict = dict(zip(self.feature_columns, self.model.feature_importances_))
            # Sort by importance
            sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
            return sorted_importance[:10]  # Return top 10 features
        return []

# Global predictor instance
predictor = None

def get_predictor():
    """Get or create the global predictor instance"""
    global predictor
    if predictor is None:
        predictor = BlackFridayPredictor()
    return predictor
