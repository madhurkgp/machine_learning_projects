import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

class PorePressurePredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = ['GR', 'RHOB', 'Vp', 'Vsh', 'Caliper', 'Porosity', 'Resistivity', 'Stress']
        self.model_path = os.path.join(os.path.dirname(__file__), '..', 'models')
        os.makedirs(self.model_path, exist_ok=True)
        
    def train_model(self):
        """Train the Random Forest model with the well data"""
        try:
            # Load and combine all well data
            wells = []
            for i in range(1, 9):
                file_path = os.path.join(os.path.dirname(__file__), '..', f'well {i}.csv')
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path)
                    wells.append(df)
            
            if not wells:
                raise Exception("No well data files found")
                
            df = pd.concat(wells, ignore_index=True)
            
            # Data preprocessing - outlier removal
            df = df.copy()
            df.loc[df['GR'] < 70, 'GR'] = np.nan
            df.loc[df['RHOB'] < 1.5, 'RHOB'] = np.nan
            df.loc[df['Vp'] > 1.70, 'Vp'] = np.nan
            df.loc[df['Vsh'] < 0.37, 'Vsh'] = np.nan
            df.loc[df['Caliper'] > 11, 'Caliper'] = np.nan
            df.loc[df['Porosity'] > 75, 'Porosity'] = np.nan
            df.loc[df['Resistivity'] > 1.5, 'Resistivity'] = np.nan
            
            df = df.dropna()
            
            # Prepare features
            X = df[self.feature_columns]
            y = df['PP']
            
            # Scale features
            self.scaler = MinMaxScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Train Random Forest model
            self.model = RandomForestRegressor(
                n_estimators=800,
                min_samples_split=2,
                min_samples_leaf=1,
                max_features='auto',
                max_depth=100,
                bootstrap=True,
                random_state=42
            )
            
            self.model.fit(X_scaled, y)
            
            # Save model and scaler
            joblib.dump(self.model, os.path.join(self.model_path, 'rf_model.pkl'))
            joblib.dump(self.scaler, os.path.join(self.model_path, 'scaler.pkl'))
            
            return True
            
        except Exception as e:
            print(f"Error training model: {str(e)}")
            return False
    
    def load_model(self):
        """Load pre-trained model and scaler"""
        try:
            model_file = os.path.join(self.model_path, 'rf_model.pkl')
            scaler_file = os.path.join(self.model_path, 'scaler.pkl')
            
            if os.path.exists(model_file) and os.path.exists(scaler_file):
                self.model = joblib.load(model_file)
                self.scaler = joblib.load(scaler_file)
                return True
            else:
                # Train model if files don't exist
                return self.train_model()
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def predict(self, depth, gr, rhob, vp, vsh, caliper, porosity, resistivity, stress):
        """Make prediction for pore pressure"""
        try:
            if self.model is None or self.scaler is None:
                if not self.load_model():
                    raise Exception("Model not available")
            
            # Prepare input data
            input_data = pd.DataFrame([{
                'GR': gr,
                'RHOB': rhob,
                'Vp': vp,
                'Vsh': vsh,
                'Caliper': caliper,
                'Porosity': porosity,
                'Resistivity': resistivity,
                'Stress': stress
            }])
            
            # Scale input
            input_scaled = self.scaler.transform(input_data)
            
            # Make prediction
            prediction = self.model.predict(input_scaled)[0]
            
            # Calculate confidence based on feature ranges
            confidence = self._calculate_confidence(input_data)
            
            return float(prediction), float(confidence)
            
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            # Return fallback prediction
            return 1700.0, 0.5
    
    def _calculate_confidence(self, input_data):
        """Calculate confidence score based on input ranges"""
        try:
            # Simple confidence calculation based on feature ranges
            confidence = 1.0
            
            # Check if features are within reasonable ranges
            if input_data['GR'].iloc[0] < 70 or input_data['GR'].iloc[0] > 150:
                confidence *= 0.8
            if input_data['RHOB'].iloc[0] < 1.5 or input_data['RHOB'].iloc[0] > 3.0:
                confidence *= 0.8
            if input_data['Vp'].iloc[0] < 1.0 or input_data['Vp'].iloc[0] > 1.7:
                confidence *= 0.8
            if input_data['Vsh'].iloc[0] < 0.37 or input_data['Vsh'].iloc[0] > 1.0:
                confidence *= 0.8
            if input_data['Caliper'].iloc[0] > 11:
                confidence *= 0.8
            if input_data['Porosity'].iloc[0] > 75:
                confidence *= 0.8
            if input_data['Resistivity'].iloc[0] > 1.5:
                confidence *= 0.8
                
            return max(0.3, min(1.0, confidence))
            
        except:
            return 0.7

# Global predictor instance
predictor = PorePressurePredictor()
