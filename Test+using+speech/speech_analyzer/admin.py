from django.contrib import admin
from .models import AudioAnalysis, WordFrequency


@admin.register(AudioAnalysis)
class AudioAnalysisAdmin(admin.ModelAdmin):
    list_display = ['audio_file_name', 'word_count', 'unique_words', 'words_per_minute', 'created_at']
    list_filter = ['created_at', 'word_count', 'unique_words']
    search_fields = ['transcribed_text', 'audio_file']
    readonly_fields = ['created_at', 'audio_duration']
    ordering = ['-created_at']
    
    def audio_file_name(self, obj):
        return obj.audio_file.name.split('/')[-1] if obj.audio_file else 'No file'
    audio_file_name.short_description = 'File Name'


@admin.register(WordFrequency)
class WordFrequencyAdmin(admin.ModelAdmin):
    list_display = ['word', 'frequency', 'audio_analysis']
    list_filter = ['frequency']
    search_fields = ['word']
    ordering = ['-frequency', 'word']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('audio_analysis')
