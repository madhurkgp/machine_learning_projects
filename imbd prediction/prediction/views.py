from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .ml_model import IMDBRatingPredictor
from .forms import MoviePredictionForm

# Initialize the predictor
predictor = IMDBRatingPredictor()
predictor.load_model()

def home(request):
    """Home page with the prediction form"""
    form = MoviePredictionForm()
    context = {
        'form': form,
        'title': 'IMDB Movie Rating Predictor'
    }
    return render(request, 'prediction/home.html', context)

@csrf_exempt
def predict(request):
    """Handle prediction requests"""
    if request.method == 'POST':
        try:
            # Parse form data
            data = {
                'num_critic_for_reviews': float(request.POST.get('num_critic_for_reviews', 140)),
                'duration': float(request.POST.get('duration', 107)),
                'director_facebook_likes': float(request.POST.get('director_facebook_likes', 686)),
                'actor_3_facebook_likes': float(request.POST.get('actor_3_facebook_likes', 645)),
                'actor_1_facebook_likes': float(request.POST.get('actor_1_facebook_likes', 6560)),
                'gross': float(request.POST.get('gross', 48468410)),
                'num_voted_users': float(request.POST.get('num_voted_users', 83668)),
                'cast_total_facebook_likes': float(request.POST.get('cast_total_facebook_likes', 9699)),
                'facenumber_in_poster': float(request.POST.get('facenumber_in_poster', 1)),
                'num_user_for_reviews': float(request.POST.get('num_user_for_reviews', 273)),
                'budget': float(request.POST.get('budget', 39752620)),
                'title_year': float(request.POST.get('title_year', 2002)),
                'actor_2_facebook_likes': float(request.POST.get('actor_2_facebook_likes', 1652)),
                'aspect_ratio': float(request.POST.get('aspect_ratio', 2.22)),
                'movie_facebook_likes': float(request.POST.get('movie_facebook_likes', 7526)),
                'color': request.POST.get('color', 'Color'),
                'content_rating': request.POST.get('content_rating', 'PG-13'),
                'language': request.POST.get('language', 'English'),
                'country': request.POST.get('country', 'USA')
            }
            
            # Make prediction
            rating, confidence = predictor.predict_rating(data)
            
            if rating is not None:
                # Determine rating category
                if rating >= 8.0:
                    category = "Excellent"
                    color_class = "excellent"
                elif rating >= 7.0:
                    category = "Good"
                    color_class = "good"
                elif rating >= 6.0:
                    category = "Average"
                    color_class = "average"
                elif rating >= 5.0:
                    category = "Below Average"
                    color_class = "below-average"
                else:
                    category = "Poor"
                    color_class = "poor"
                
                result = {
                    'success': True,
                    'predicted_rating': rating,
                    'confidence': confidence,
                    'category': category,
                    'color_class': color_class
                }
            else:
                result = {
                    'success': False,
                    'error': 'Model not available. Please train the model first.'
                }
                
        except Exception as e:
            result = {
                'success': False,
                'error': f'Prediction error: {str(e)}'
            }
        
        return JsonResponse(result)

def sample_data(request):
    """Return sample movie data for testing"""
    sample_movies = [
        {
            'name': 'Avatar',
            'data': {
                'num_critic_for_reviews': 723,
                'duration': 178,
                'director_facebook_likes': 0,
                'actor_3_facebook_likes': 855,
                'actor_1_facebook_likes': 1000,
                'gross': 760505847,
                'num_voted_users': 886204,
                'cast_total_facebook_likes': 4834,
                'facenumber_in_poster': 0,
                'num_user_for_reviews': 3054,
                'budget': 237000000,
                'title_year': 2009,
                'actor_2_facebook_likes': 936,
                'aspect_ratio': 1.78,
                'movie_facebook_likes': 33000,
                'color': 'Color',
                'content_rating': 'PG-13',
                'language': 'English',
                'country': 'USA'
            }
        },
        {
            'name': 'The Dark Knight',
            'data': {
                'num_critic_for_reviews': 813,
                'duration': 164,
                'director_facebook_likes': 22000,
                'actor_3_facebook_likes': 23000,
                'actor_1_facebook_likes': 27000,
                'gross': 448130642,
                'num_voted_users': 1144337,
                'cast_total_facebook_likes': 106759,
                'facenumber_in_poster': 0,
                'num_user_for_reviews': 2701,
                'budget': 250000000,
                'title_year': 2012,
                'actor_2_facebook_likes': 23000,
                'aspect_ratio': 2.35,
                'movie_facebook_likes': 164000,
                'color': 'Color',
                'content_rating': 'PG-13',
                'language': 'English',
                'country': 'USA'
            }
        }
    ]
    
    return JsonResponse({'samples': sample_movies})
