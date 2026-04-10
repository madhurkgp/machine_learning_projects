from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min, Sum
import json
import pandas as pd
from datetime import datetime, timedelta
from .models import CovidData, Prediction, ModelMetrics
from .ml_model import predictor
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

def home(request):
    """Home page with COVID-19 dashboard"""
    # Get latest statistics
    latest_data = CovidData.objects.all().order_by('-date_recorded')[:10]
    total_stats = CovidData.objects.aggregate(
        total_active=Sum('active_cases'),
        total_positive=Sum('positive_cases'),
        total_cured=Sum('cured_cases'),
        total_death=Sum('death_cases')
    )
    
    # Get recent predictions
    recent_predictions = Prediction.objects.all().order_by('-prediction_date')[:5]
    
    context = {
        'latest_data': latest_data,
        'total_stats': total_stats,
        'recent_predictions': recent_predictions,
        'page_title': 'COVID-19 Analysis Dashboard'
    }
    return render(request, 'prediction/home.html', context)

def prediction_form(request):
    """Prediction form page"""
    if request.method == 'POST':
        try:
            # Get form data
            input_data = {
                'active_cases': int(request.POST.get('active_cases', 0)),
                'positive_cases': int(request.POST.get('positive_cases', 0)),
                'cured_cases': int(request.POST.get('cured_cases', 0)),
                'death_cases': int(request.POST.get('death_cases', 0)),
                'new_active': int(request.POST.get('new_active', 0)),
                'new_positive': int(request.POST.get('new_positive', 0)),
                'new_cured': int(request.POST.get('new_cured', 0)),
                'new_death': int(request.POST.get('new_death', 0))
            }
            
            # Validate input
            is_valid, errors = predictor.validate_input(input_data)
            if not is_valid:
                messages.error(request, f"Validation errors: {', '.join(errors)}")
                return render(request, 'prediction/prediction_form.html', {
                    'form_data': input_data,
                    'errors': errors
                })
            
            # Make prediction
            result = predictor.predict(input_data)
            
            if result['status'] == 'success':
                # Save prediction to database
                prediction = Prediction.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    state_name=request.POST.get('state_name', 'Unknown'),
                    predicted_active=result['predicted_active'],
                    predicted_positive=result['predicted_positive'],
                    predicted_cured=result['predicted_cured'],
                    predicted_death=result['predicted_death'],
                    confidence_score=result['confidence_score'],
                    input_data=input_data
                )
                
                context = {
                    'prediction': prediction,
                    'input_data': input_data,
                    'result': result,
                    'page_title': 'Prediction Results'
                }
                return render(request, 'prediction/prediction_result.html', context)
            else:
                messages.error(request, f"Prediction failed: {result.get('error', 'Unknown error')}")
                
        except ValueError as e:
            messages.error(request, "Please enter valid numeric values")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, 'prediction/prediction_form.html', {
        'page_title': 'COVID-19 Prediction'
    })

@csrf_exempt
@require_http_methods(["POST"])
def api_predict(request):
    """API endpoint for predictions"""
    try:
        data = json.loads(request.body)
        
        # Validate input
        is_valid, errors = predictor.validate_input(data)
        if not is_valid:
            return JsonResponse({
                'status': 'error',
                'errors': errors
            }, status=400)
        
        # Make prediction
        result = predictor.predict(data)
        
        if result['status'] == 'success':
            # Save prediction
            prediction = Prediction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                state_name=data.get('state_name', 'Unknown'),
                predicted_active=result['predicted_active'],
                predicted_positive=result['predicted_positive'],
                predicted_cured=result['predicted_cured'],
                predicted_death=result['predicted_death'],
                confidence_score=result['confidence_score'],
                input_data=data
            )
            
            return JsonResponse({
                'status': 'success',
                'prediction_id': prediction.id,
                'results': result
            })
        else:
            return JsonResponse(result, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)

def data_visualization(request):
    """Data visualization page"""
    # Get data for charts
    data = CovidData.objects.all().order_by('date_recorded')
    
    # Prepare data for charts
    dates = [d.date_recorded.strftime('%Y-%m-%d') for d in data]
    active_cases = [d.active_cases for d in data]
    positive_cases = [d.positive_cases for d in data]
    cured_cases = [d.cured_cases for d in data]
    death_cases = [d.death_cases for d in data]
    
    context = {
        'dates': json.dumps(dates),
        'active_cases': json.dumps(active_cases),
        'positive_cases': json.dumps(positive_cases),
        'cured_cases': json.dumps(cured_cases),
        'death_cases': json.dumps(death_cases),
        'page_title': 'Data Visualization'
    }
    return render(request, 'prediction/visualization.html', context)

def predictions_history(request):
    """View prediction history"""
    predictions = Prediction.objects.all().order_by('-prediction_date')
    
    # Pagination
    paginator = Paginator(predictions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': 'Prediction History'
    }
    return render(request, 'prediction/history.html', context)

def model_info(request):
    """Model information and metrics"""
    # Get feature importance
    feature_importance = predictor.get_feature_importance()
    
    # Get model metrics if available
    model_metrics = ModelMetrics.objects.all().order_by('-training_date').first()
    
    context = {
        'feature_importance': feature_importance,
        'model_metrics': model_metrics,
        'page_title': 'Model Information'
    }
    return render(request, 'prediction/model_info.html', context)

def load_sample_data(request):
    """Load sample COVID-19 data"""
    if request.method == 'POST':
        try:
            # Sample data based on the notebook
            sample_states = [
                {'state_name': 'Maharashtra', 'active_cases': 55351, 'positive_cases': 1969114, 
                 'cured_cases': 1863702, 'death_cases': 50061, 'new_active': 53463, 
                 'new_positive': 1971552, 'new_cured': 1867988, 'new_death': 50101, 'state_code': '27'},
                {'state_name': 'Kerala', 'active_cases': 64379, 'positive_cases': 811148, 
                 'cured_cases': 743467, 'death_cases': 3302, 'new_active': 63547, 
                 'new_positive': 814258, 'new_cured': 747389, 'new_death': 3322, 'state_code': '32'},
                {'state_name': 'Karnataka', 'active_cases': 9668, 'positive_cases': 927559, 
                 'cured_cases': 905751, 'death_cases': 12140, 'new_active': 9363, 
                 'new_positive': 928055, 'new_cured': 906548, 'new_death': 12144, 'state_code': '29'},
            ]
            
            # Clear existing data
            CovidData.objects.all().delete()
            
            # Add sample data
            for state_data in sample_states:
                CovidData.objects.create(**state_data)
            
            messages.success(request, 'Sample data loaded successfully!')
            
        except Exception as e:
            messages.error(request, f'Error loading sample data: {str(e)}')
    
    return redirect('home')
