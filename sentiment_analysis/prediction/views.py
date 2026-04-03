from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator
from .models import SentimentPrediction
from .forms import SentimentAnalysisForm
from .ml_model import sentiment_analyzer
import json

def home(request):
    if request.method == 'POST':
        form = SentimentAnalysisForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            
            try:
                # Get prediction from ML model
                result = sentiment_analyzer.predict_sentiment(text)
                
                # Save prediction to database
                prediction = SentimentPrediction.objects.create(
                    text=text,
                    prediction=result['prediction'],
                    confidence=result['confidence']
                )
                
                context = {
                    'form': SentimentAnalysisForm(),
                    'result': result,
                    'input_text': text,
                    'recent_predictions': SentimentPrediction.objects.all()[:5]
                }
                
                return render(request, 'prediction/result.html', context)
                
            except Exception as e:
                messages.error(request, f'Error analyzing sentiment: {str(e)}')
                return redirect('home')
    else:
        form = SentimentAnalysisForm()
    
    context = {
        'form': form,
        'recent_predictions': SentimentPrediction.objects.all()[:5]
    }
    return render(request, 'prediction/home.html', context)

@csrf_exempt
def api_predict(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            
            if not text.strip():
                return JsonResponse({
                    'error': 'Text cannot be empty'
                }, status=400)
            
            result = sentiment_analyzer.predict_sentiment(text)
            
            # Save prediction
            prediction = SentimentPrediction.objects.create(
                text=text,
                prediction=result['prediction'],
                confidence=result['confidence']
            )
            
            return JsonResponse({
                'prediction': result['prediction'],
                'confidence': result['confidence'],
                'id': prediction.id
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

def history(request):
    predictions = SentimentPrediction.objects.all()
    paginator = Paginator(predictions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj
    }
    return render(request, 'prediction/history.html', context)

def sample_texts(request):
    sample_data = [
        "This movie was absolutely amazing! The acting was superb and the storyline kept me engaged throughout.",
        "I was really disappointed with this film. The plot was predictable and the acting was terrible.",
        "The movie was okay, nothing special but not terrible either. It had some good moments.",
        "One of the worst movies I've ever seen. Complete waste of time and money.",
        "An incredible cinematic experience! Beautiful visuals, great performances, and a touching story."
    ]
    
    return JsonResponse({'samples': sample_data})
