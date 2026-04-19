from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .models import AudioFile, AudioAnalysis
from .forms import AudioUploadForm
from .services import AudioProcessor

def home(request):
    """Home page with upload form and recent analyses"""
    form = AudioUploadForm()
    recent_analyses = AudioAnalysis.objects.select_related('audio_file').order_by('-analysis_date')[:5]
    
    context = {
        'form': form,
        'recent_analyses': recent_analyses,
    }
    return render(request, 'audio_app/home.html', context)

def upload_audio(request):
    """Handle audio file upload"""
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                audio_file = form.save()
                messages.success(request, f'Audio file "{audio_file.name}" uploaded successfully!')
                return redirect('analyze_audio')
            except Exception as e:
                messages.error(request, f'Error uploading file: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AudioUploadForm()
    
    return redirect('home')

def analyze_audio(request):
    """Analyze uploaded audio files"""
    if request.method == 'POST':
        audio_file_id = request.POST.get('audio_file_id')
        if audio_file_id:
            audio_file = get_object_or_404(AudioFile, id=audio_file_id)
            
            try:
                processor = AudioProcessor()
                analysis = processor.process_audio_file(audio_file)
                messages.success(request, 'Audio analysis completed successfully!')
                return redirect('analysis_results', analysis_id=analysis.id)
            except Exception as e:
                messages.error(request, f'Error analyzing audio: {str(e)}')
        else:
            messages.error(request, 'Please select an audio file to analyze.')
    
    # Get all unanalyzed audio files
    unanalyzed_files = AudioFile.objects.filter(
        audioanalysis__isnull=True
    ).order_by('-upload_date')
    
    context = {
        'unanalyzed_files': unanalyzed_files,
    }
    return render(request, 'audio_app/analyze.html', context)

def analysis_results(request, analysis_id):
    """Display analysis results"""
    analysis = get_object_or_404(AudioAnalysis, id=analysis_id)
    processor = AudioProcessor()
    insights = processor.get_audio_insights(analysis)
    
    context = {
        'analysis': analysis,
        'insights': insights,
    }
    return render(request, 'audio_app/results.html', context)

def load_sample_data(request):
    """Load sample audio data for testing"""
    try:
        # Create a sample audio file entry (you would need an actual sample file)
        sample_file_path = 'Code and Files/file_example_WAV_2MG.wav'
        
        try:
            audio_file = AudioFile.objects.create(
                name='Sample Audio File',
                audio_file=sample_file_path
            )
            
            # Process the sample
            processor = AudioProcessor()
            analysis = processor.process_audio_file(audio_file)
            
            return JsonResponse({
                'success': True,
                'message': 'Sample data loaded successfully!',
                'analysis_id': analysis.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error loading sample data: {str(e)}'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })
