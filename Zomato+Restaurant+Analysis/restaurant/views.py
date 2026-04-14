import json
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Avg
from .models import RestaurantPrediction, ModelMetrics
from .ml_models import RestaurantRatingPredictor
from .forms import RestaurantPredictionForm


def home(request):
    """Home page with prediction form"""
    if request.method == 'POST':
        form = RestaurantPredictionForm(request.POST)
        if form.is_valid():
            try:
                # Get form data
                data = form.cleaned_data
                
                # Make prediction
                predictor = RestaurantRatingPredictor()
                prediction_result = predictor.predict_rating(data)
                
                # Save prediction to database
                prediction = RestaurantPrediction.objects.create(
                    online_order=data['online_order'],
                    book_table=data['book_table'],
                    votes=data['votes'],
                    location=data['location'],
                    rest_type=data['rest_type'],
                    cuisines=data['cuisines'],
                    approx_cost=data['approx_cost'],
                    predicted_rating=prediction_result['predicted_rating'],
                    model_used=prediction_result['model_used'],
                    confidence_score=prediction_result.get('confidence_score'),
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                messages.success(request, f'Prediction successful! Rating: {prediction_result["predicted_rating"]:.2f}/5.0')
                return redirect('prediction_result', pk=prediction.pk)
                
            except Exception as e:
                messages.error(request, f'Error making prediction: {str(e)}')
    else:
        form = RestaurantPredictionForm()
    
    # Get recent predictions for display
    recent_predictions = RestaurantPrediction.objects.all()[:5]
    
    # Get model metrics
    metrics = ModelMetrics.objects.all()
    best_model = metrics.order_by('-r2_score').first() if metrics else None
    
    context = {
        'form': form,
        'recent_predictions': recent_predictions,
        'best_model': best_model,
        'page_title': 'Zomato Restaurant Rating Predictor'
    }
    return render(request, 'restaurant/home.html', context)


def prediction_result(request, pk):
    """Display detailed prediction result"""
    prediction = RestaurantPrediction.objects.get(pk=pk)
    
    # Get similar predictions
    similar_predictions = RestaurantPrediction.objects.filter(
        location=prediction.location,
        rest_type=prediction.rest_type
    ).exclude(pk=pk)[:3]
    
    context = {
        'prediction': prediction,
        'similar_predictions': similar_predictions,
        'page_title': 'Prediction Result'
    }
    return render(request, 'restaurant/result.html', context)


def predictions_history(request):
    """Display all predictions with pagination"""
    predictions = RestaurantPrediction.objects.all()
    
    # Filter by model if specified
    model_filter = request.GET.get('model')
    if model_filter:
        predictions = predictions.filter(model_used=model_filter)
    
    # Pagination
    paginator = Paginator(predictions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get statistics
    stats = {
        'total_predictions': RestaurantPrediction.objects.count(),
        'avg_rating': RestaurantPrediction.objects.aggregate(Avg('predicted_rating'))['predicted_rating__avg'] or 0,
        'avg_confidence': RestaurantPrediction.objects.aggregate(Avg('confidence_score'))['confidence_score__avg'] or 0,
    }
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'model_filter': model_filter,
        'page_title': 'Prediction History'
    }
    return render(request, 'restaurant/history.html', context)


def analytics(request):
    """Display analytics and insights"""
    # Get top locations by prediction count
    top_locations = RestaurantPrediction.objects.values('location').annotate(
        count=models.Count('id'),
        avg_rating=models.Avg('predicted_rating')
    ).order_by('-count')[:10]
    
    # Get model performance comparison
    model_stats = {}
    for model in ['LinearRegression', 'RandomForest', 'DecisionTree']:
        model_predictions = RestaurantPrediction.objects.filter(model_used=model)
        if model_predictions.exists():
            model_stats[model] = {
                'count': model_predictions.count(),
                'avg_rating': model_predictions.aggregate(Avg('predicted_rating'))['predicted_rating__avg'] or 0,
                'avg_confidence': model_predictions.aggregate(Avg('confidence_score'))['confidence_score__avg'] or 0,
            }
    
    # Rating distribution
    rating_dist = {}
    for i in range(1, 6):
        rating_dist[f'{i}.0-{i+1}.0'] = RestaurantPrediction.objects.filter(
            predicted_rating__gte=i,
            predicted_rating__lt=i+1
        ).count()
    
    context = {
        'top_locations': top_locations,
        'model_stats': model_stats,
        'rating_dist': rating_dist,
        'page_title': 'Analytics Dashboard'
    }
    return render(request, 'restaurant/analytics.html', context)


@csrf_exempt
def predict_api(request):
    """API endpoint for predictions"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['online_order', 'book_table', 'votes', 'location', 'rest_type', 'cuisines', 'approx_cost']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
        
        # Make prediction
        predictor = RestaurantRatingPredictor()
        result = predictor.predict_rating(data)
        
        return JsonResponse(result, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def load_sample_data(request):
    """Load sample data for testing"""
    sample_data = {
        'online_order': True,
        'book_table': False,
        'votes': 150,
        'location': 'BTM',
        'rest_type': 'Quick Bites',
        'cuisines': 'North Indian, Chinese',
        'approx_cost': 300
    }
    
    form = RestaurantPredictionForm(initial=sample_data)
    messages.info(request, 'Sample data loaded. Click "Predict Rating" to see results.')
    
    return render(request, 'restaurant/home.html', {'form': form, 'page_title': 'Zomato Restaurant Rating Predictor'})
