import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import os

def train_and_save_model():
    print("Loading training data...")
    df = pd.read_csv('Notebook/train.csv')
    
    print("Preprocessing data...")
    # Data preprocessing (same as in notebook)
    df['Product_ID'] = df['Product_ID'].str.replace('P00', '')
    ss = StandardScaler()
    df['Product_ID'] = ss.fit_transform(df['Product_ID'].values.reshape(-1, 1))
    
    # Drop Product_Category_3 due to too many missing values
    df.drop(['Product_Category_3'], axis=1, inplace=True)
    
    # Fill missing values in Product_Category_2 with mean
    df['Product_Category_2'] = df['Product_Category_2'].fillna(df['Product_Category_2'].mean())
    
    # Label encoding for categorical variables
    cat_cols = ['Gender', 'City_Category', 'Age']
    le = LabelEncoder()
    for i in cat_cols:
        df[i] = le.fit_transform(df[i])
    
    # Handle Stay_In_Current_City_Years
    df['Stay_In_Current_City_Years'] = df['Stay_In_Current_City_Years'].replace('4+', '4')
    df['Stay_In_Current_City_Years'] = df['Stay_In_Current_City_Years'].astype(int)
    
    # Convert types
    df['Gender'] = df['Gender'].astype(int)
    df['Age'] = df['Age'].astype(int)
    df['City_Category'] = df['City_Category'].astype('category')
    
    # Apply log transformation to Purchase
    df['Purchase'] = np.log(df['Purchase'])
    
    # Create dummy variables
    df = pd.get_dummies(df)
    
    # Prepare features and target
    X = df.drop(labels=['Purchase'], axis=1)
    Y = df['Purchase']
    
    # Split data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    print("Training Random Forest model...")
    # Train Random Forest model with fewer trees for memory efficiency
    model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=15)
    model.fit(X_train, Y_train)
    
    # Evaluate model
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    
    train_rmse = np.sqrt(mean_squared_error(Y_train, train_preds))
    test_rmse = np.sqrt(mean_squared_error(Y_test, test_preds))
    train_r2 = model.score(X_train, Y_train)
    test_r2 = model.score(X_test, Y_test)
    
    print(f"Training RMSE: {train_rmse:.4f}")
    print(f"Test RMSE: {test_rmse:.4f}")
    print(f"Training R²: {train_r2:.4f}")
    print(f"Test R²: {test_r2:.4f}")
    
    # Save model and preprocessing objects
    print("Saving model and preprocessing objects...")
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
    
    # Save the model, scaler, and label encoders
    joblib.dump(model, 'models/random_forest_model.pkl')
    joblib.dump(scaler, 'models/feature_scaler.pkl')
    joblib.dump(ss, 'models/product_id_scaler.pkl')
    
    # Save label encoders - we need to create new ones and fit them properly
    # For the web app, we'll create fresh label encoders in the prediction module
    # Here we just save the original data mappings for reference
    original_data_info = {
        'gender_values': ['F', 'M'],
        'age_values': ['0-17', '18-25', '26-35', '36-45', '46-50', '51-55', '55+'],
        'city_category_values': ['A', 'B', 'C']
    }
    joblib.dump(original_data_info, 'models/original_data_info.pkl')
    
    # Save feature columns for prediction
    feature_columns = X.columns.tolist()
    joblib.dump(feature_columns, 'models/feature_columns.pkl')
    
    # Save preprocessing info
    preprocessing_info = {
        'product_category_2_mean': df['Product_Category_2'].mean(),
        'categorical_columns': cat_cols,
        'numerical_columns': ['User_ID', 'Occupation', 'Marital_Status', 'Product_Category_1', 'Product_Category_2', 'Stay_In_Current_City_Years']
    }
    joblib.dump(preprocessing_info, 'models/preprocessing_info.pkl')
    
    print("Model and preprocessing objects saved successfully!")
    print("Files saved in 'models' directory:")
    print("- random_forest_model.pkl")
    print("- feature_scaler.pkl") 
    print("- product_id_scaler.pkl")
    print("- original_data_info.pkl")
    print("- feature_columns.pkl")
    print("- preprocessing_info.pkl")

if __name__ == "__main__":
    train_and_save_model()
