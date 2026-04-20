import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import AudioAnalysis, WordFrequency
from .forms import AudioUploadForm, AudioAnalysisForm
from .services import SpeechAnalyzerService
import json


def home(request):
    """Home page with audio upload form"""
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_analysis = form.save()
            return redirect('analyze_audio', pk=audio_analysis.pk)
    else:
        form = AudioUploadForm()
    
    return render(request, 'speech_analyzer/home.html', {'form': form})


def analyze_audio(request, pk):
    """Analyze uploaded audio file"""
    audio_analysis = get_object_or_404(AudioAnalysis, pk=pk)
    
    if request.method == 'POST':
        # Perform analysis
        service = SpeechAnalyzerService()
        result = service.analyze_audio_file(audio_analysis.audio_file.path)
        
        if result['success']:
            # Update audio analysis with results
            audio_analysis.transcribed_text = result['transcribed_text']
            audio_analysis.word_count = result['word_count']
            audio_analysis.unique_words = result['unique_words']
            audio_analysis.words_per_minute = result['words_per_minute']
            audio_analysis.audio_duration = result['audio_duration']
            audio_analysis.save()
            
            # Save word frequencies
            WordFrequency.objects.filter(audio_analysis=audio_analysis).delete()
            for word, frequency in result['word_frequencies'].items():
                WordFrequency.objects.create(
                    audio_analysis=audio_analysis,
                    word=word,
                    frequency=frequency
                )
            
            messages.success(request, 'Audio analysis completed successfully!')
            return redirect('analysis_results', pk=audio_analysis.pk)
        else:
            messages.error(request, f'Analysis failed: {result["error"]}')
    
    return render(request, 'speech_analyzer/analyze.html', {'audio_analysis': audio_analysis})


def analysis_results(request, pk):
    """Display analysis results"""
    audio_analysis = get_object_or_404(AudioAnalysis, pk=pk)
    word_frequencies = audio_analysis.word_frequencies.all()[:20]  # Top 20 words
    
    # Generate insights
    service = SpeechAnalyzerService()
    if audio_analysis.transcribed_text:
        insights = service._generate_insights(
            audio_analysis.transcribed_text.split(),
            audio_analysis.word_count,
            audio_analysis.unique_words,
            audio_analysis.words_per_minute
        )
    else:
        insights = []
    
    context = {
        'audio_analysis': audio_analysis,
        'word_frequencies': word_frequencies,
        'insights': insights
    }
    
    return render(request, 'speech_analyzer/results.html', context)


def history(request):
    """Display analysis history"""
    analyses = AudioAnalysis.objects.all().order_by('-created_at')
    paginator = Paginator(analyses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'speech_analyzer/history.html', {'page_obj': page_obj})


@require_POST
def delete_analysis(request, pk):
    """Delete an analysis"""
    audio_analysis = get_object_or_404(AudioAnalysis, pk=pk)
    audio_file = audio_analysis.audio_file.path
    
    try:
        # Delete audio file
        if os.path.exists(audio_file):
            os.remove(audio_file)
        
        # Delete database record
        audio_analysis.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            messages.success(request, 'Analysis deleted successfully!')
            return redirect('history')
            
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': str(e)})
        else:
            messages.error(request, f'Error deleting analysis: {e}')
            return redirect('history')


def sample_data(request):
    """Load sample audio data for testing"""
    try:
        # Copy sample audio file to media directory
        import shutil
        from django.conf import settings
        
        source_path = os.path.join(settings.BASE_DIR, 'Code and Files', 'voice-data.wav')
        if os.path.exists(source_path):
            # Create a new audio analysis with sample data
            service = SpeechAnalyzerService()
            result = service.analyze_audio_file(source_path)
            
            if result['success']:
                # Copy file to media directory
                media_path = os.path.join(settings.MEDIA_ROOT, 'audio_files')
                os.makedirs(media_path, exist_ok=True)
                dest_path = os.path.join(media_path, 'sample_voice.wav')
                shutil.copy2(source_path, dest_path)
                
                # Create analysis record
                audio_analysis = AudioAnalysis.objects.create(
                    audio_file=f'audio_files/sample_voice.wav',
                    transcribed_text=result['transcribed_text'],
                    word_count=result['word_count'],
                    unique_words=result['unique_words'],
                    words_per_minute=result['words_per_minute'],
                    audio_duration=result['audio_duration']
                )
                
                # Save word frequencies
                for word, frequency in result['word_frequencies'].items():
                    WordFrequency.objects.create(
                        audio_analysis=audio_analysis,
                        word=word,
                        frequency=frequency
                    )
                
                messages.success(request, 'Sample data loaded successfully!')
                return redirect('analysis_results', pk=audio_analysis.pk)
            else:
                messages.error(request, f'Error analyzing sample data: {result["error"]}')
        else:
            messages.error(request, 'Sample audio file not found!')
            
    except Exception as e:
        messages.error(request, f'Error loading sample data: {e}')
    
    return redirect('home')
