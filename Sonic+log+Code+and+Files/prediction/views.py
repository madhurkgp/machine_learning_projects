from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import SonicLogPrediction
from .forms import SonicLogPredictionForm
from .ml_models import predictor

def home(request):
    """
    Home page with prediction form
    """
    if request.method == 'POST':
        form = SonicLogPredictionForm(request.POST)
        if form.is_valid():
            # Get form data
            input_data = {
                'cal': [form.cleaned_data['cal']],
                'cnc': [form.cleaned_data['cnc']],
                'gr': [form.cleaned_data['gr']],
                'hrd': [form.cleaned_data['hrd']],
                'hrm': [form.cleaned_data['hrm']],
                'pe': [form.cleaned_data['pe']],
                'zden': [form.cleaned_data['zden']],
            }
            
            # Make prediction
            try:
                prediction_result = predictor.predict(input_data, use_wavelet=True)
                
                # Save to database
                prediction = form.save(commit=False)
                prediction.dtc_predicted = prediction_result['dtc']
                prediction.dts_predicted = prediction_result['dts']
                prediction.prediction_method = prediction_result['method']
                prediction.save()
                
                messages.success(request, 'Prediction completed successfully!')
                
                return render(request, 'prediction/result.html', {
                    'prediction': prediction,
                    'form': SonicLogPredictionForm(),
                })
                
            except Exception as e:
                messages.error(request, f'Prediction error: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SonicLogPredictionForm()
    
    # Get recent predictions
    recent_predictions = SonicLogPrediction.objects.all()[:10]
    
    return render(request, 'prediction/home.html', {
        'form': form,
        'recent_predictions': recent_predictions,
    })

def prediction_history(request):
    """
    View all prediction history
    """
    predictions = SonicLogPrediction.objects.all()
    
    # Pagination
    paginator = Paginator(predictions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'prediction/history.html', {
        'page_obj': page_obj,
    })

def prediction_detail(request, prediction_id):
    """
    View detailed prediction
    """
    prediction = SonicLogPrediction.objects.get(id=prediction_id)
    return render(request, 'prediction/detail.html', {
        'prediction': prediction,
    })

@csrf_exempt
def api_predict(request):
    """
    API endpoint for predictions
    """
    if request.method == 'POST':
        try:
            # Extract data from request
            input_data = {
                'cal': [float(request.POST.get('cal', 0))],
                'cnc': [float(request.POST.get('cnc', 0))],
                'gr': [float(request.POST.get('gr', 0))],
                'hrd': [float(request.POST.get('hrd', 0))],
                'hrm': [float(request.POST.get('hrm', 0))],
                'pe': [float(request.POST.get('pe', 0))],
                'zden': [float(request.POST.get('zden', 0))],
            }
            
            # Make prediction
            prediction_result = predictor.predict(input_data, use_wavelet=True)
            
            return JsonResponse({
                'success': True,
                'dtc': prediction_result['dtc'],
                'dts': prediction_result['dts'],
                'method': prediction_result['method'],
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e),
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST method allowed',
    })

def sample_data(request):
    """
    Load sample data for testing
    """
    sample_inputs = [
        {
            'cal': 8.5781,
            'cnc': 0.3521,
            'gr': 55.1824,
            'hrd': 0.8121,
            'hrm': 0.7810,
            'pe': 6.8291,
            'zden': 2.3256,
        },
        {
            'cal': 8.6250,
            'cnc': 0.1936,
            'gr': 36.8218,
            'hrd': 1.6230,
            'hrm': 1.6281,
            'pe': 4.9415,
            'zden': 2.4322,
        },
        {
            'cal': 9.0489,
            'cnc': 0.3372,
            'gr': 58.3462,
            'hrd': 3.1583,
            'hrm': 3.2806,
            'pe': 7.8567,
            'zden': 2.5514,
        },
    ]
    
    # Pick a random sample
    import random
    sample = random.choice(sample_inputs)
    
    form = SonicLogPredictionForm(initial=sample)
    
    return render(request, 'prediction/home.html', {
        'form': form,
        'recent_predictions': SonicLogPrediction.objects.all()[:10],
        'sample_loaded': True,
    })

def about(request):
    """
    About page with project information
    """
    return render(request, 'prediction/about.html')
