from django.db import models
from django.utils import timezone

class AudioFile(models.Model):
    name = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio_files/')
    upload_date = models.DateTimeField(default=timezone.now)
    duration = models.FloatField(null=True, blank=True)
    sample_rate = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class AudioAnalysis(models.Model):
    audio_file = models.ForeignKey(AudioFile, on_delete=models.CASCADE)
    analysis_date = models.DateTimeField(default=timezone.now)
    
    # Time domain features
    amplitude_envelope_avg = models.FloatField(null=True, blank=True)
    zero_crossing_rate_avg = models.FloatField(null=True, blank=True)
    rms_energy_avg = models.FloatField(null=True, blank=True)
    
    # Frequency domain features
    spectral_centroid_avg = models.FloatField(null=True, blank=True)
    spectral_bandwidth_avg = models.FloatField(null=True, blank=True)
    spectral_rolloff_avg = models.FloatField(null=True, blank=True)
    
    # MFCC features
    mfcc_features = models.JSONField(null=True, blank=True)
    
    # Additional metadata
    frame_size = models.IntegerField(default=1024)
    hop_length = models.IntegerField(default=512)
    
    def __str__(self):
        return f"Analysis of {self.audio_file.name} on {self.analysis_date.strftime('%Y-%m-%d %H:%M')}"
