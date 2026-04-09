from django.db import models

class AirQualityPrediction(models.Model):
    so2 = models.FloatField(help_text="Sulphur Dioxide concentration (µg/m³)")
    no2 = models.FloatField(help_text="Nitrogen Dioxide concentration (µg/m³)")
    rspm = models.FloatField(help_text="Respirable Suspended Particulate Matter (µg/m³)")
    spm = models.FloatField(help_text="Suspended Particulate Matter (µg/m³)")
    aqi_value = models.FloatField(null=True, blank=True)
    aqi_category = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prediction from {self.created_at.strftime('%Y-%m-%d %H:%M')}"
