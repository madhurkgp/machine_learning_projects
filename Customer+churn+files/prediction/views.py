import joblib
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

# Load the trained model and artifacts
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models')

try:
    model = joblib.load(os.path.join(MODEL_PATH, 'random_forest_model.pkl'))
    label_encoder = joblib.load(os.path.join(MODEL_PATH, 'label_encoder.pkl'))
    feature_names = joblib.load(os.path.join(MODEL_PATH, 'feature_names.pkl'))
    MODEL_LOADED = True
except Exception as e:
    print(f"Error loading model: {e}")
    MODEL_LOADED = False

def home(request):
    """Render the home page with prediction form"""
    context = {
        'geography_options': ['France', 'Germany', 'Spain'],
        'gender_options': ['Male', 'Female'],
        'model_loaded': MODEL_LOADED
    }
    return render(request, 'prediction/home.html', context)

def predict_churn(request):
    """Handle churn prediction requests"""
    if not MODEL_LOADED:
        return JsonResponse({
            'error': 'Model not loaded. Please check server configuration.'
        }, status=500)
    
    if request.method == 'POST':
        try:
            # Get form data
            data = json.loads(request.body)
            
            # Process input data
            credit_score = int(data['credit_score'])
            geography = data['geography']
            gender = data['gender']
            age = int(data['age'])
            tenure = int(data['tenure'])
            balance = float(data['balance'])
            num_products = int(data['num_products'])
            has_cr_card = int(data['has_cr_card'])
            is_active_member = int(data['is_active_member'])
            estimated_salary = float(data['estimated_salary'])
            
            # Encode categorical variables
            geography_encoded = label_encoder.transform([geography])[0] if geography in label_encoder.classes_ else 0
            gender_encoded = label_encoder.transform([gender])[0] if gender in label_encoder.classes_ else 0
            
            # Create feature array in the correct order
            features = np.array([[
                credit_score, geography_encoded, gender_encoded, age, tenure,
                balance, num_products, has_cr_card, is_active_member, estimated_salary
            ]])
            
            # Make prediction
            prediction = model.predict(features)[0]
            prediction_proba = model.predict_proba(features)[0]
            
            # Calculate confidence score
            confidence = max(prediction_proba) * 100
            
            # Determine risk level
            if prediction == 1:
                risk_level = "High" if confidence > 75 else "Medium"
                result_text = "Customer is likely to churn"
            else:
                risk_level = "Low"
                result_text = "Customer is likely to stay"
            
            return JsonResponse({
                'prediction': int(prediction),
                'confidence': round(confidence, 2),
                'risk_level': risk_level,
                'result_text': result_text,
                'probability_churn': round(prediction_proba[1] * 100, 2),
                'probability_stay': round(prediction_proba[0] * 100, 2)
            })
            
        except Exception as e:
            return JsonResponse({
                'error': f'Prediction error: {str(e)}'
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_sample_data(request):
    """Return sample data for testing"""
    sample_data = {
        'credit_score': 650,
        'geography': 'France',
        'gender': 'Female',
        'age': 42,
        'tenure': 5,
        'balance': 75000,
        'num_products': 2,
        'has_cr_card': 1,
        'is_active_member': 1,
        'estimated_salary': 100000
    }
    return JsonResponse(sample_data)
