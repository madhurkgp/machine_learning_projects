from django.db import models

class SentimentPrediction(models.Model):
    text = models.TextField()
    prediction = models.CharField(max_length=20)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.text[:50]}... - {self.prediction}"
