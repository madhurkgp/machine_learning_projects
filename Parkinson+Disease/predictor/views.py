from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import joblib
import numpy as np
from .forms import ParkinsonPredictionForm

# Load the trained model and feature names
try:
    model = joblib.load('parkinson_model.joblib')
    feature_names = joblib.load('feature_names.joblib')
    model_loaded = True
except:
    model = None
    feature_names = None
    model_loaded = False

def home(request):
    """Home page with the prediction form"""
    form = ParkinsonPredictionForm()
    context = {
        'form': form,
        'model_loaded': model_loaded,
        'title': 'Parkinson\'s Disease Prediction',
        'description': 'Predict Parkinson\'s disease using voice analysis with machine learning'
    }
    return render(request, 'predictor/home.html', context)

def predict(request):
    """Handle prediction form submission"""
    if request.method == 'POST':
        form = ParkinsonPredictionForm(request.POST)
        
        if form.is_valid():
            if not model_loaded:
                return JsonResponse({
                    'success': False,
                    'error': 'Model not loaded. Please check server configuration.'
                })
            
            try:
                # Get features from form
                features = form.get_features_array()
                
                # Make prediction
                prediction = model.predict(features)[0]
                prediction_proba = model.predict_proba(features)[0]
                
                # Prepare result
                result = {
                    'success': True,
                    'prediction': int(prediction),
                    'prediction_label': 'Parkinson\'s Disease' if prediction == 1 else 'Healthy',
                    'confidence': float(max(prediction_proba) * 100),
                    'probabilities': {
                        'healthy': float(prediction_proba[0] * 100),
                        'parkinsons': float(prediction_proba[1] * 100)
                    }
                }
                
                return JsonResponse(result)
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': f'Prediction error: {str(e)}'
                })
        else:
            # Return form validation errors
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(error) for error in error_list]
            
            return JsonResponse({
                'success': False,
                'errors': errors
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

@csrf_exempt
def sample_data(request):
    """Return sample data for testing"""
    if request.method == 'GET':
        # Sample data from the dataset (both healthy and Parkinson's cases)
        sample_data = [
            {
                'name': 'Healthy Sample',
                'data': {
                    'mdvp_fo': 174.188,
                    'mdvp_fhi': 230.978,
                    'mdvp_flo': 94.261,
                    'mdvp_jitter': 0.00459,
                    'mdvp_jitter_abs': 0.00003,
                    'mdvp_rap': 0.00263,
                    'mdvp_ppq': 0.00259,
                    'jitter_ddp': 0.00790,
                    'mdvp_shimmer': 0.04087,
                    'mdvp_shimmer_db': 0.327,
                    'shimmer_apq3': 0.01717,
                    'shimmer_apq5': 0.02183,
                    'mdvp_apq': 0.02453,
                    'shimmer_dda': 0.07008,
                    'nhr': 0.02764,
                    'hnr': 19.517,
                    'rpde': 0.448439,
                    'dfa': 0.657899,
                    'spread1': -6.538586,
                    'spread2': 0.121952,
                    'd2': 2.657476,
                    'ppe': 0.133050
                }
            },
            {
                'name': 'Parkinson\'s Sample',
                'data': {
                    'mdvp_fo': 119.992,
                    'mdvp_fhi': 157.302,
                    'mdvp_flo': 74.997,
                    'mdvp_jitter': 0.00784,
                    'mdvp_jitter_abs': 0.00007,
                    'mdvp_rap': 0.00370,
                    'mdvp_ppq': 0.00554,
                    'jitter_ddp': 0.01109,
                    'mdvp_shimmer': 0.04374,
                    'mdvp_shimmer_db': 0.426,
                    'shimmer_apq3': 0.02182,
                    'shimmer_apq5': 0.03130,
                    'mdvp_apq': 0.02971,
                    'shimmer_dda': 0.06545,
                    'nhr': 0.02211,
                    'hnr': 21.033,
                    'rpde': 0.414783,
                    'dfa': 0.815285,
                    'spread1': -4.813031,
                    'spread2': 0.266482,
                    'd2': 2.301442,
                    'ppe': 0.284654
                }
            }
        ]
        
        return JsonResponse({'samples': sample_data})
    
    return JsonResponse({'error': 'Invalid request method'})

def about(request):
    """About page with information about the project"""
    context = {
        'title': 'About Parkinson\'s Disease Prediction',
        'description': 'Learn about voice analysis for Parkinson\'s disease detection'
    }
    return render(request, 'predictor/about.html', context)
