from django.db import models
from django.core.validators import FileExtensionValidator
import os


class AudioClassification(models.Model):
    AUDIO_FORMATS = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
    
    audio_file = models.FileField(
        upload_to='audio_files/',
        validators=[FileExtensionValidator(allowed_extensions=['wav', 'mp3', 'flac', 'm4a', 'ogg'])],
        help_text="Upload audio file (WAV, MP3, FLAC, M4A, OGG)"
    )
    filename = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text="File size in bytes")
    duration = models.FloatField(null=True, blank=True, help_text="Audio duration in seconds")
    
    # Audio features
    mfcc_features = models.JSONField(null=True, blank=True, help_text="MFCC features extracted from audio")
    zcr_features = models.JSONField(null=True, blank=True, help_text="Zero Crossing Rate features")
    
    # Classification results
    predicted_class = models.CharField(max_length=100, null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True, help_text="Processing time in seconds")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Audio Classification"
        verbose_name_plural = "Audio Classifications"
    
    def __str__(self):
        return f"{self.filename} - {self.predicted_class or 'Not processed'}"
    
    def get_file_extension(self):
        return os.path.splitext(self.filename)[1].lower()
    
    def get_formatted_file_size(self):
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} MB"


class ClassificationResult(models.Model):
    audio_classification = models.ForeignKey(AudioClassification, on_delete=models.CASCADE, related_name='results')
    class_name = models.CharField(max_length=100)
    probability = models.FloatField()
    
    class Meta:
        ordering = ['-probability']
        verbose_name = "Classification Result"
        verbose_name_plural = "Classification Results"
    
    def __str__(self):
        return f"{self.class_name}: {self.probability:.2%}"
