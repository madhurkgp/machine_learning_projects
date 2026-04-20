from django.db import models
from django.utils import timezone


class AudioAnalysis(models.Model):
    """Model to store audio analysis results"""
    audio_file = models.FileField(upload_to='audio_files/')
    transcribed_text = models.TextField(blank=True, null=True)
    word_count = models.IntegerField(default=0)
    unique_words = models.IntegerField(default=0)
    words_per_minute = models.FloatField(default=0.0)
    audio_duration = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Analysis of {self.audio_file.name}"
    
    class Meta:
        ordering = ['-created_at']


class WordFrequency(models.Model):
    """Model to store word frequency analysis"""
    audio_analysis = models.ForeignKey(AudioAnalysis, on_delete=models.CASCADE, related_name='word_frequencies')
    word = models.CharField(max_length=100)
    frequency = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.word}: {self.frequency}"
    
    class Meta:
        ordering = ['-frequency', 'word']
