from django.contrib import admin
from .models import AudioClassification, ClassificationResult


@admin.register(AudioClassification)
class AudioClassificationAdmin(admin.ModelAdmin):
    list_display = [
        'filename', 'predicted_class', 'confidence_score', 
        'file_size', 'duration', 'created_at', 'processed_at'
    ]
    list_filter = [
        'predicted_class', 'created_at', 'processed_at'
    ]
    search_fields = ['filename', 'predicted_class']
    readonly_fields = [
        'created_at', 'processed_at', 'processing_time', 
        'mfcc_features', 'zcr_features'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Audio Information', {
            'fields': ('audio_file', 'filename', 'file_size', 'duration')
        }),
        ('Classification Results', {
            'fields': ('predicted_class', 'confidence_score', 'processing_time')
        }),
        ('Extracted Features', {
            'fields': ('mfcc_features', 'zcr_features'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'processed_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('results')


@admin.register(ClassificationResult)
class ClassificationResultAdmin(admin.ModelAdmin):
    list_display = ['audio_classification', 'class_name', 'probability']
    list_filter = ['class_name']
    search_fields = ['class_name', 'audio_classification__filename']
    ordering = ['-probability']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('audio_classification')
