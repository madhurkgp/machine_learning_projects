import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
import warnings
warnings.filterwarnings("ignore")

def calculate_so2_index(so2):
    si = 0
    if so2 <= 40:
        si = so2 * (50/40)
    elif so2 > 40 and so2 <= 80:
        si = 50 + (so2 - 40) * (50/40)
    elif so2 > 80 and so2 <= 380:
        si = 100 + (so2 - 80) * (100/300)
    elif so2 > 380 and so2 <= 800:
        si = 200 + (so2 - 380) * (100/420)
    elif so2 > 800 and so2 <= 1600:
        si = 300 + (so2 - 800) * (100/800)
    elif so2 > 1600:
        si = 400 + (so2 - 1600) * (100/800)
    return si

def calculate_no2_index(no2):
    ni = 0
    if no2 <= 40:
        ni = no2 * 50/40
    elif no2 > 40 and no2 <= 80:
        ni = 50 + (no2 - 40) * (50/40)
    elif no2 > 80 and no2 <= 180:
        ni = 100 + (no2 - 80) * (100/100)
    elif no2 > 180 and no2 <= 280:
        ni = 200 + (no2 - 180) * (100/100)
    elif no2 > 280 and no2 <= 400:
        ni = 300 + (no2 - 280) * (100/120)
    else:
        ni = 400 + (no2 - 400) * (100/120)
    return ni

def calculate_rspm_index(rspm):
    rpi = 0
    if rspm <= 30:
        rpi = rspm * 50/30
    elif rspm > 30 and rspm <= 60:
        rpi = 50 + (rspm - 30) * 50/30
    elif rspm > 60 and rspm <= 90:
        rpi = 100 + (rspm - 60) * 100/30
    elif rspm > 90 and rspm <= 120:
        rpi = 200 + (rspm - 90) * 100/30
    elif rspm > 120 and rspm <= 250:
        rpi = 300 + (rspm - 120) * (100/130)
    else:
        rpi = 400 + (rspm - 250) * (100/130)
    return rpi

def calculate_spm_index(spm):
    spi = 0
    if spm <= 50:
        spi = spm * 50/50
    elif spm > 50 and spm <= 100:
        spi = 50 + (spm - 50) * (50/50)
    elif spm > 100 and spm <= 250:
        spi = 100 + (spm - 100) * (100/150)
    elif spm > 250 and spm <= 350:
        spi = 200 + (spm - 250) * (100/100)
    elif spm > 350 and spm <= 430:
        spi = 300 + (spm - 350) * (100/80)
    else:
        spi = 400 + (spm - 430) * (100/430)
    return spi

def calculate_aqi(si, ni, rpi, spi):
    aqi = 0
    if si > ni and si > rpi and si > spi:
        aqi = si
    if ni > si and ni > rpi and ni > spi:
        aqi = ni
    if rpi > si and rpi > ni and rpi > spi:
        aqi = rpi
    if spi > si and spi > ni and spi > rpi:
        aqi = spi
    return aqi

def get_aqi_range(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi > 50 and aqi <= 100:
        return "Moderate"
    elif aqi > 100 and aqi <= 200:
        return "Poor"
    elif aqi > 200 and aqi <= 300:
        return "Unhealthy"
    elif aqi > 300 and aqi <= 400:
        return "Very unhealthy"
    elif aqi > 400:
        return "Hazardous"

def main():
    print("Loading and processing data...")
    
    # Load data
    df = pd.read_csv('Note Book/data.csv', encoding='unicode_escape')
    
    # Drop unnecessary columns
    df.drop(['agency', 'stn_code', 'date', 'sampling_date', 'location_monitoring_station'], axis=1, inplace=True)
    
    # Handle missing values
    df['location'] = df['location'].fillna(df['location'].mode()[0])
    df['type'] = df['type'].fillna(df['type'].mode()[0])
    df.fillna(0, inplace=True)
    
    # Calculate pollutant indices
    print("Calculating pollutant indices...")
    df['SOi'] = df['so2'].apply(calculate_so2_index)
    df['Noi'] = df['no2'].apply(calculate_no2_index)
    df['Rpi'] = df['rspm'].apply(calculate_rspm_index)
    df['SPMi'] = df['spm'].apply(calculate_spm_index)
    df['AQI'] = df.apply(lambda x: calculate_aqi(x['SOi'], x['Noi'], x['Rpi'], x['SPMi']), axis=1)
    df['AQI_Range'] = df['AQI'].apply(get_aqi_range)
    
    # Prepare features and targets
    X = df[['SOi', 'Noi', 'Rpi', 'SPMi']]
    y_regression = df['AQI']
    y_classification = df['AQI_Range']
    
    # Split data
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X, y_regression, test_size=0.2, random_state=70
    )
    X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
        X, y_classification, test_size=0.33, random_state=70
    )
    
    print("Training models...")
    
    # Train regression models
    rf_reg = RandomForestRegressor(random_state=70)
    rf_reg.fit(X_train_reg, y_train_reg)
    
    # Train classification models
    rf_clf = RandomForestClassifier(random_state=70)
    rf_clf.fit(X_train_clf, y_train_clf)
    
    print("Saving models...")
    
    # Save models
    joblib.dump(rf_reg, 'models/rf_regression_model.pkl')
    joblib.dump(rf_clf, 'models/rf_classification_model.pkl')
    
    # Save feature names for consistency
    joblib.dump(list(X.columns), 'models/feature_names.pkl')
    
    print("Models saved successfully!")
    print(f"Regression model R² score: {rf_reg.score(X_test_reg, y_test_reg):.4f}")
    print(f"Classification model accuracy: {rf_clf.score(X_test_clf, y_test_clf):.4f}")

if __name__ == "__main__":
    main()
