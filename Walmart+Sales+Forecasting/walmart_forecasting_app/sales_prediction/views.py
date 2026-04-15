from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import SalesPrediction
from .forms import SalesPredictionForm
from .ml_model import predictor
import os

def home(request):
    """Home page with prediction form"""
    form = SalesPredictionForm()
    
    # Get recent predictions for display
    recent_predictions = SalesPrediction.objects.all()[:5]
    
    context = {
        'form': form,
        'recent_predictions': recent_predictions,
        'page_title': 'Walmart Sales Forecasting'
    }
    return render(request, 'sales_prediction/home.html', context)

def predict_sales(request):
    """Handle prediction request"""
    if request.method == 'POST':
        form = SalesPredictionForm(request.POST)
        if form.is_valid():
            # Extract form data
            store = form.cleaned_data['store']
            department = form.cleaned_data['department']
            is_holiday = form.cleaned_data['is_holiday']
            temperature = form.cleaned_data['temperature']
            cpi = form.cleaned_data['cpi']
            unemployment = form.cleaned_data['unemployment']
            size = form.cleaned_data['size']
            week = form.cleaned_data['week']
            year = form.cleaned_data['year']
            
            # Make prediction
            prediction, confidence, error = predictor.predict(
                store, department, is_holiday, temperature, 
                cpi, unemployment, size, week, year
            )
            
            if error:
                messages.error(request, f'Prediction error: {error}')
                return redirect('home')
            
            # Save prediction to database
            sales_prediction = form.save(commit=False)
            sales_prediction.predicted_sales = round(prediction, 2)
            sales_prediction.confidence_score = round(confidence, 4)
            sales_prediction.save()
            
            messages.success(request, f'Prediction successful! Estimated sales: ${prediction:,.2f}')
            return redirect('prediction_result', pk=sales_prediction.pk)
        else:
            messages.error(request, 'Please correct the errors in the form.')
    
    return redirect('home')

def prediction_result(request, pk):
    """Display prediction result"""
    try:
        prediction = SalesPrediction.objects.get(pk=pk)
        context = {
            'prediction': prediction,
            'page_title': 'Prediction Result'
        }
        return render(request, 'sales_prediction/result.html', context)
    except SalesPrediction.DoesNotExist:
        messages.error(request, 'Prediction not found.')
        return redirect('home')

def prediction_history(request):
    """Display prediction history"""
    predictions = SalesPrediction.objects.all()
    paginator = Paginator(predictions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': 'Prediction History'
    }
    return render(request, 'sales_prediction/history.html', context)

def sample_data(request):
    """Load sample data for testing"""
    if request.method == 'POST':
        try:
            # Try to load actual data if available
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..', 'Walmart Sales Forecasting')
            success = predictor.load_and_train_models(data_path)
            
            if not success:
                # Fallback to sample data
                success = predictor.load_and_train_models()
            
            if success:
                messages.success(request, 'Models trained successfully with sample data!')
            else:
                messages.error(request, 'Failed to train models.')
        except Exception as e:
            messages.error(request, f'Error loading data: {str(e)}')
    
    return redirect('home')

def api_predict(request):
    """API endpoint for predictions"""
    if request.method == 'POST':
        try:
            data = request.POST
            
            prediction, confidence, error = predictor.predict(
                int(data.get('store')),
                int(data.get('department')),
                data.get('is_holiday').lower() == 'true',
                float(data.get('temperature')),
                float(data.get('cpi')),
                float(data.get('unemployment')),
                int(data.get('size')),
                int(data.get('week')),
                int(data.get('year'))
            )
            
            if error:
                return JsonResponse({'error': error}, status=400)
            
            return JsonResponse({
                'predicted_sales': round(prediction, 2),
                'confidence_score': round(confidence, 4),
                'model_used': 'ridge'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
