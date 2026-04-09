import joblib
import numpy as np
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import AirQualityPredictionForm
from .models import AirQualityPrediction
import os

# Load models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models')

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

def get_aqi_color(aqi_range):
    colors = {
        "Good": "#00e400",
        "Moderate": "#ffff00", 
        "Poor": "#ff7e00",
        "Unhealthy": "#ff0000",
        "Very unhealthy": "#8f3f97",
        "Hazardous": "#7e0023"
    }
    return colors.get(aqi_range, "#808080")

def home(request):
    if request.method == 'POST':
        form = AirQualityPredictionForm(request.POST)
        if form.is_valid():
            try:
                # Get form data
                so2 = form.cleaned_data['so2']
                no2 = form.cleaned_data['no2']
                rspm = form.cleaned_data['rspm']
                spm = form.cleaned_data['spm']
                
                # Calculate pollutant indices
                soi = calculate_so2_index(so2)
                noi = calculate_no2_index(no2)
                rpi = calculate_rspm_index(rspm)
                spmi = calculate_spm_index(spm)
                
                # Load models
                rf_reg = joblib.load(os.path.join(MODEL_PATH, 'rf_regression_model.pkl'))
                rf_clf = joblib.load(os.path.join(MODEL_PATH, 'rf_classification_model.pkl'))
                
                # Make predictions
                features = np.array([[soi, noi, rpi, spmi]])
                aqi_value = rf_reg.predict(features)[0]
                aqi_category = rf_clf.predict(features)[0]
                
                # Save prediction
                prediction = form.save(commit=False)
                prediction.aqi_value = round(aqi_value, 2)
                prediction.aqi_category = aqi_category
                prediction.save()
                
                # Get color for category
                aqi_color = get_aqi_color(aqi_category)
                
                context = {
                    'form': form,
                    'prediction': prediction,
                    'aqi_color': aqi_color,
                    'aqi_category_class': aqi_category.lower().replace(' ', ''),
                    'pollutant_indices': {
                        'SOi': round(soi, 2),
                        'Noi': round(noi, 2),
                        'Rpi': round(rpi, 2),
                        'SPMi': round(spmi, 2)
                    }
                }
                
                messages.success(request, 'Air quality prediction completed successfully!')
                return render(request, 'prediction/home.html', context)
                
            except Exception as e:
                messages.error(request, f'An error occurred during prediction: {str(e)}')
    else:
        form = AirQualityPredictionForm()
    
    # Get recent predictions
    recent_predictions = AirQualityPrediction.objects.all()[:10]
    
    context = {
        'form': form,
        'recent_predictions': recent_predictions
    }
    
    return render(request, 'prediction/home.html', context)

def sample_data(request):
    """Provide sample data for testing"""
    sample_data = [
        {'so2': 15.2, 'no2': 25.8, 'rspm': 45.3, 'spm': 78.5},
        {'so2': 8.5, 'no2': 18.2, 'rspm': 32.1, 'spm': 55.7},
        {'so2': 45.8, 'no2': 67.3, 'rspm': 89.4, 'spm': 123.6},
        {'so2': 3.2, 'no2': 12.5, 'rspm': 28.9, 'spm': 41.2},
        {'so2': 78.9, 'no2': 89.4, 'rspm': 156.7, 'spm': 234.8}
    ]
    
    import random
    selected_sample = random.choice(sample_data)
    
    form = AirQualityPredictionForm(initial=selected_sample)
    
    recent_predictions = AirQualityPrediction.objects.all()[:10]
    
    context = {
        'form': form,
        'recent_predictions': recent_predictions,
        'sample_filled': True
    }
    
    return render(request, 'prediction/home.html', context)

@csrf_exempt
def predict_api(request):
    """API endpoint for predictions"""
    if request.method == 'POST':
        try:
            data = request.POST
            
            # Get values
            so2 = float(data.get('so2', 0))
            no2 = float(data.get('no2', 0))
            rspm = float(data.get('rspm', 0))
            spm = float(data.get('spm', 0))
            
            # Calculate indices
            soi = calculate_so2_index(so2)
            noi = calculate_no2_index(no2)
            rpi = calculate_rspm_index(rspm)
            spmi = calculate_spm_index(spm)
            
            # Load models
            rf_reg = joblib.load(os.path.join(MODEL_PATH, 'rf_regression_model.pkl'))
            rf_clf = joblib.load(os.path.join(MODEL_PATH, 'rf_classification_model.pkl'))
            
            # Make predictions
            features = np.array([[soi, noi, rpi, spmi]])
            aqi_value = rf_reg.predict(features)[0]
            aqi_category = rf_clf.predict(features)[0]
            
            return JsonResponse({
                'success': True,
                'aqi_value': round(float(aqi_value), 2),
                'aqi_category': aqi_category,
                'aqi_color': get_aqi_color(aqi_category),
                'pollutant_indices': {
                    'SOi': round(float(soi), 2),
                    'Noi': round(float(noi), 2),
                    'Rpi': round(float(rpi), 2),
                    'SPMi': round(float(spmi), 2)
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
