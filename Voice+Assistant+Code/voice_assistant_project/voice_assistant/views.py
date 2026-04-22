import json
import time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from .models import VoiceInteraction, VoiceCommand
from .services import VoiceAssistantService


def home(request):
    """Home page with voice assistant interface"""
    service = VoiceAssistantService()
    greeting = service.get_greeting_message()
    suggestions = service.get_command_suggestions()
    
    # Get recent interactions
    recent_interactions = VoiceInteraction.objects.all()[:5]
    
    context = {
        'greeting': greeting,
        'command_suggestions': suggestions,
        'recent_interactions': recent_interactions,
        'page_title': 'Voice Assistant - Dave'
    }
    return render(request, 'voice_assistant/home.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def process_voice_command(request):
    """Process voice command from AJAX request"""
    start_time = time.time()
    service = VoiceAssistantService()
    
    try:
        data = json.loads(request.body)
        command_text = data.get('command', '').strip()
        
        if not command_text:
            return JsonResponse({
                'success': False,
                'error': 'No command provided'
            })
        
        # Process the command
        response_data = service.process_command(command_text)
        
        # Calculate response time
        response_time = int((time.time() - start_time) * 1000)
        
        # Save interaction to database
        interaction = service.save_interaction(
            voice_command=command_text,
            transcribed_text=command_text,
            response_data=response_data,
            confidence_score=1.0,  # Text input has perfect confidence
            response_time=response_time
        )
        
        # Try to speak the response (optional, may not work in web context)
        # service.speak(response_data['response'])
        
        return JsonResponse({
            'success': True,
            'response': response_data['response'],
            'command_type': response_data['command_type'],
            'action_taken': response_data['action_taken'],
            'response_time_ms': response_time,
            'interaction_id': interaction.id if interaction else None
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Processing error: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def test_microphone(request):
    """Test microphone access"""
    service = VoiceAssistantService()
    is_accessible, message = service.test_microphone_access()
    
    return JsonResponse({
        'success': is_accessible,
        'message': message
    })


def command_history(request):
    """Display command history with pagination"""
    interactions = VoiceInteraction.objects.all()
    
    # Filter by command type if specified
    command_type = request.GET.get('type')
    if command_type:
        interactions = interactions.filter(command_type=command_type)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        interactions = interactions.filter(
            transcribed_text__icontains=search_query
        )
    
    # Pagination
    paginator = Paginator(interactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get command type counts for sidebar
    command_counts = VoiceInteraction.objects.values('command_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'page_obj': page_obj,
        'command_counts': command_counts,
        'current_type': command_type,
        'search_query': search_query,
        'page_title': 'Command History'
    }
    return render(request, 'voice_assistant/history.html', context)


def analytics(request):
    """Display analytics dashboard"""
    # Get statistics
    total_interactions = VoiceInteraction.objects.count()
    successful_interactions = VoiceInteraction.objects.filter(is_successful=True).count()
    success_rate = (successful_interactions / total_interactions * 100) if total_interactions > 0 else 0
    
    # Command type distribution
    command_stats = VoiceInteraction.objects.values('command_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Recent activity
    recent_interactions = VoiceInteraction.objects.all()[:10]
    
    # Average response time
    avg_response_time = VoiceInteraction.objects.aggregate(
        avg_time=models.Avg('response_time_ms')
    )['avg_time'] or 0
    
    context = {
        'total_interactions': total_interactions,
        'successful_interactions': successful_interactions,
        'success_rate': round(success_rate, 2),
        'command_stats': command_stats,
        'recent_interactions': recent_interactions,
        'avg_response_time': round(avg_response_time, 2),
        'page_title': 'Analytics Dashboard'
    }
    return render(request, 'voice_assistant/analytics.html', context)


def clear_history(request):
    """Clear all voice interaction history"""
    if request.method == 'POST':
        VoiceInteraction.objects.all().delete()
        messages.success(request, 'Command history cleared successfully!')
        return redirect('command_history')
    
    return render(request, 'voice_assistant/clear_history.html', {
        'page_title': 'Clear History'
    })


def help_page(request):
    """Help and documentation page"""
    service = VoiceAssistantService()
    suggestions = service.get_command_suggestions()
    
    context = {
        'command_suggestions': suggestions,
        'page_title': 'Help & Documentation'
    }
    return render(request, 'voice_assistant/help.html', context)
