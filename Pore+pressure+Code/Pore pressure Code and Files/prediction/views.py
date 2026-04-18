from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import PredictionHistory
from .forms import PredictionForm
from .ml_model import predictor
import json

def home(request):
    """Home page with prediction form"""
    form = PredictionForm()
    recent_predictions = PredictionHistory.objects.all().order_by('-created_at')[:5]
    context = {
        'form': form,
        'recent_predictions': recent_predictions,
        'title': 'Pore Pressure Prediction System'
    }
    return render(request, 'prediction/home.html', context)

def predict(request):
    """Handle prediction form submission"""
    if request.method == 'POST':
        try:
            # Get form data
            depth = float(request.POST.get('depth'))
            gr = float(request.POST.get('gr'))
            rhob = float(request.POST.get('rhob'))
            vp = float(request.POST.get('vp'))
            vsh = float(request.POST.get('vsh'))
            caliper = float(request.POST.get('caliper'))
            porosity = float(request.POST.get('porosity'))
            resistivity = float(request.POST.get('resistivity'))
            stress = float(request.POST.get('stress'))
            
            # Make prediction
            predicted_pp, confidence = predictor.predict(
                depth, gr, rhob, vp, vsh, caliper, porosity, resistivity, stress
            )
            
            # Save to database
            prediction = PredictionHistory.objects.create(
                depth=depth,
                gr=gr,
                rhob=rhob,
                vp=vp,
                vsh=vsh,
                caliper=caliper,
                porosity=porosity,
                resistivity=resistivity,
                stress=stress,
                predicted_pp=predicted_pp,
                confidence_score=confidence
            )
            
            messages.success(request, f'Prediction successful! Pore Pressure: {predicted_pp:.2f} PSI')
            
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Error making prediction: {str(e)}')
            return redirect('home')
    
    return redirect('home')

@csrf_exempt
def api_predict(request):
    """API endpoint for predictions"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['depth', 'gr', 'rhob', 'vp', 'vsh', 'caliper', 'porosity', 'resistivity', 'stress']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
            
            # Make prediction
            predicted_pp, confidence = predictor.predict(
                float(data['depth']),
                float(data['gr']),
                float(data['rhob']),
                float(data['vp']),
                float(data['vsh']),
                float(data['caliper']),
                float(data['porosity']),
                float(data['resistivity']),
                float(data['stress'])
            )
            
            # Save to database
            prediction = PredictionHistory.objects.create(
                depth=float(data['depth']),
                gr=float(data['gr']),
                rhob=float(data['rhob']),
                vp=float(data['vp']),
                vsh=float(data['vsh']),
                caliper=float(data['caliper']),
                porosity=float(data['porosity']),
                resistivity=float(data['resistivity']),
                stress=float(data['stress']),
                predicted_pp=predicted_pp,
                confidence_score=confidence
            )
            
            return JsonResponse({
                'success': True,
                'predicted_pp': predicted_pp,
                'confidence_score': confidence,
                'prediction_id': prediction.id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def get_sample_data(request):
    """Get sample data for testing"""
    sample_data = {
        'depth': 100.0,
        'gr': 85.5,
        'rhob': 2.1,
        'vp': 1.5,
        'vsh': 0.65,
        'caliper': 8.5,
        'porosity': 45.0,
        'resistivity': 0.9,
        'stress': 1500000.0
    }
    return JsonResponse(sample_data)
