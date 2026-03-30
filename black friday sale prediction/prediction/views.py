from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .forms import PredictionForm
from .ml_utils import get_predictor

logger = logging.getLogger(__name__)

def home(request):
    """Home page with prediction form"""
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            try:
                # Get the predictor instance
                predictor = get_predictor()
                
                # Make prediction
                prediction = predictor.predict(form.cleaned_data)
                
                # Get feature importance for display
                feature_importance = predictor.get_feature_importance()
                
                context = {
                    'form': form,
                    'prediction': prediction,
                    'feature_importance': feature_importance,
                    'success': True
                }
                
                messages.success(request, f'Predicted purchase amount: ${prediction:,}')
                return render(request, 'prediction/home.html', context)
                
            except Exception as e:
                logger.error(f"Prediction error: {str(e)}")
                messages.error(request, f'An error occurred during prediction: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PredictionForm()
    
    context = {
        'form': form,
        'success': False
    }
    
    return render(request, 'prediction/home.html', context)

@csrf_exempt
def api_predict(request):
    """API endpoint for AJAX predictions"""
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            # Validate data using form
            form = PredictionForm(data)
            if not form.is_valid():
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
            
            # Get the predictor instance
            predictor = get_predictor()
            
            # Make prediction
            prediction = predictor.predict(form.cleaned_data)
            
            return JsonResponse({
                'success': True,
                'prediction': prediction,
                'formatted_prediction': f'${prediction:,}'
            })
            
        except Exception as e:
            logger.error(f"API prediction error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST method allowed'
    }, status=405)

def sample_data(request):
    """Return sample data for testing"""
    sample_data = {
        'user_id': 1000001,
        'product_id': 'P00069042',
        'gender': 'M',
        'age': '26-35',
        'occupation': 10,
        'city_category': 'A',
        'stay_years': '2',
        'marital_status': 0,
        'product_category_1': 3,
        'product_category_2': 6.0
    }
    return JsonResponse(sample_data)

def about(request):
    """About page with model information"""
    try:
        predictor = get_predictor()
        feature_importance = predictor.get_feature_importance()
        
        context = {
            'feature_importance': feature_importance,
            'model_info': {
                'model_type': 'Random Forest Regressor',
                'training_samples': '550,068',
                'features': len(predictor.feature_columns),
                'r2_score': '0.77',
                'rmse': '0.35'
            }
        }
    except Exception as e:
        logger.error(f"Error loading model info: {str(e)}")
        context = {
            'feature_importance': [],
            'model_info': {}
        }
    
    return render(request, 'prediction/about.html', context)
