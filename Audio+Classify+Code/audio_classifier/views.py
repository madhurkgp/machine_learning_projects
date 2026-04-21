from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils import timezone
import json
import os

from .models import AudioClassification, ClassificationResult
from .forms import AudioUploadForm, SampleDataForm
from .services import AudioClassificationService, AudioFeatureExtractor, SampleDataService


def home(request):
    """Home page with audio upload form"""
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the uploaded file
                audio_classification = form.save(commit=False)
                audio_classification.filename = request.FILES['audio_file'].name
                audio_classification.file_size = request.FILES['audio_file'].size
                
                # Get audio duration
                duration = AudioFeatureExtractor.get_audio_duration(
                    audio_classification.audio_file.path
                )
                audio_classification.duration = duration
                
                audio_classification.save()
                
                # Process the audio file
                classification_service = AudioClassificationService()
                result = classification_service.classify_audio(
                    audio_classification.audio_file.path
                )
                
                if result['success']:
                    # Update the classification record
                    audio_classification.predicted_class = result['predicted_class']
                    audio_classification.confidence_score = result['confidence_score']
                    audio_classification.processing_time = result['processing_time']
                    audio_classification.mfcc_features = result['mfcc_features']
                    audio_classification.processed_at = timezone.now()
                    audio_classification.save()
                    
                    # Save detailed results
                    for class_result in result['class_probabilities']:
                        ClassificationResult.objects.create(
                            audio_classification=audio_classification,
                            class_name=class_result['class_name'],
                            probability=class_result['probability']
                        )
                    
                    messages.success(request, 'Audio classified successfully!')
                    return redirect('classification_result', pk=audio_classification.pk)
                else:
                    messages.error(request, f'Classification failed: {result.get("error", "Unknown error")}')
                    
            except Exception as e:
                messages.error(request, f'Error processing audio file: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AudioUploadForm()
    
    # Get recent classifications
    recent_classifications = AudioClassification.objects.filter(
        predicted_class__isnull=False
    ).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'recent_classifications': recent_classifications,
        'title': 'Audio Classification'
    }
    return render(request, 'audio_classifier/home.html', context)


def classification_result(request, pk):
    """Display classification results"""
    classification = get_object_or_404(AudioClassification, pk=pk)
    results = classification.results.all()
    
    context = {
        'classification': classification,
        'results': results,
        'title': f'Classification Result - {classification.filename}'
    }
    return render(request, 'audio_classifier/result.html', context)


def classification_history(request):
    """Display classification history with pagination"""
    classifications = AudioClassification.objects.all().order_by('-created_at')
    
    paginator = Paginator(classifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'title': 'Classification History'
    }
    return render(request, 'audio_classifier/history.html', context)


def sample_data(request):
    """Handle sample data requests"""
    if request.method == 'POST':
        form = SampleDataForm(request.POST)
        if form.is_valid():
            sample_type = form.cleaned_data['sample_type']
            
            # Get sample file info
            sample_files = SampleDataService.create_sample_audio_files()
            sample_file = None
            
            for file_info in sample_files:
                if file_info['name'] == f'{sample_type}_sample':
                    sample_file = file_info
                    break
            
            if sample_file and sample_file['exists']:
                try:
                    # Create classification record for sample
                    classification = AudioClassification.objects.create(
                        audio_file=sample_file['file_path'],
                        filename=f'{sample_type}_sample.wav',
                        file_size=os.path.getsize(sample_file['file_path']),
                        duration=AudioFeatureExtractor.get_audio_duration(sample_file['file_path'])
                    )
                    
                    # Process the sample
                    classification_service = AudioClassificationService()
                    result = classification_service.classify_audio(sample_file['file_path'])
                    
                    if result['success']:
                        classification.predicted_class = result['predicted_class']
                        classification.confidence_score = result['confidence_score']
                        classification.processing_time = result['processing_time']
                        classification.mfcc_features = result['mfcc_features']
                        classification.processed_at = timezone.now()
                        classification.save()
                        
                        # Save detailed results
                        for class_result in result['class_probabilities']:
                            ClassificationResult.objects.create(
                                audio_classification=classification,
                                class_name=class_result['class_name'],
                                probability=class_result['probability']
                            )
                        
                        messages.success(request, f'Sample {sample_type} classified successfully!')
                        return redirect('classification_result', pk=classification.pk)
                    else:
                        messages.error(request, f'Sample classification failed: {result.get("error", "Unknown error")}')
                        
                except Exception as e:
                    messages.error(request, f'Error processing sample: {str(e)}')
            else:
                messages.error(request, f'Sample file for {sample_type} not found. Please upload your own audio file.')
    else:
        form = SampleDataForm()
    
    # Get available sample files
    sample_files = SampleDataService.create_sample_audio_files()
    
    context = {
        'form': form,
        'sample_files': sample_files,
        'title': 'Sample Data'
    }
    return render(request, 'audio_classifier/sample_data.html', context)


@csrf_exempt
def classify_audio_api(request):
    """API endpoint for audio classification"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    if 'audio_file' not in request.FILES:
        return JsonResponse({'error': 'No audio file provided'}, status=400)
    
    try:
        audio_file = request.FILES['audio_file']
        
        # Validate file
        allowed_extensions = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
        file_extension = audio_file.name.lower().split('.')[-1]
        
        if f'.{file_extension}' not in allowed_extensions:
            return JsonResponse({'error': f'File type .{file_extension} not supported'}, status=400)
        
        if audio_file.size > 25 * 1024 * 1024:
            return JsonResponse({'error': 'File size exceeds 25MB limit'}, status=400)
        
        # Save temporary file
        temp_path = f'/tmp/{audio_file.name}'
        with open(temp_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        # Classify the audio
        classification_service = AudioClassificationService()
        result = classification_service.classify_audio(temp_path)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'predicted_class': result['predicted_class'],
                'confidence_score': result['confidence_score'],
                'class_probabilities': result['class_probabilities'],
                'processing_time': result['processing_time']
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result.get('error', 'Classification failed')
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def download_results(request, pk):
    """Download classification results as JSON"""
    classification = get_object_or_404(AudioClassification, pk=pk)
    
    results_data = {
        'filename': classification.filename,
        'file_size': classification.file_size,
        'duration': classification.duration,
        'predicted_class': classification.predicted_class,
        'confidence_score': classification.confidence_score,
        'processing_time': classification.processing_time,
        'mfcc_features': classification.mfcc_features,
        'zcr_features': classification.zcr_features,
        'created_at': classification.created_at.isoformat(),
        'processed_at': classification.processed_at.isoformat() if classification.processed_at else None,
        'detailed_results': [
            {
                'class_name': result.class_name,
                'probability': result.probability
            }
            for result in classification.results.all()
        ]
    }
    
    response = HttpResponse(
        json.dumps(results_data, indent=2),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="{classification.filename}_results.json"'
    return response
