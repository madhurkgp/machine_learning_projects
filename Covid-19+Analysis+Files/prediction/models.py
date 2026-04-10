from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CovidData(models.Model):
    """Model to store COVID-19 data for ML training and predictions"""
    state_name = models.CharField(max_length=100)
    active_cases = models.IntegerField(default=0)
    positive_cases = models.IntegerField(default=0)
    cured_cases = models.IntegerField(default=0)
    death_cases = models.IntegerField(default=0)
    new_active = models.IntegerField(default=0)
    new_positive = models.IntegerField(default=0)
    new_cured = models.IntegerField(default=0)
    new_death = models.IntegerField(default=0)
    state_code = models.CharField(max_length=5, blank=True)
    date_recorded = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date_recorded']
        verbose_name = "COVID-19 Data"
        verbose_name_plural = "COVID-19 Data"
    
    def __str__(self):
        return f"{self.state_name} - {self.date_recorded.strftime('%Y-%m-%d')}"
    
    @property
    def recovery_rate(self):
        """Calculate recovery rate"""
        if self.positive_cases == 0:
            return 0
        return round((self.cured_cases / self.positive_cases) * 100, 2)
    
    @property
    def death_rate(self):
        """Calculate death rate"""
        if self.positive_cases == 0:
            return 0
        return round((self.death_cases / self.positive_cases) * 100, 2)
    
    @property
    def active_rate(self):
        """Calculate active rate"""
        if self.positive_cases == 0:
            return 0
        return round((self.active_cases / self.positive_cases) * 100, 2)

class Prediction(models.Model):
    """Model to store ML predictions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    state_name = models.CharField(max_length=100)
    predicted_active = models.IntegerField()
    predicted_positive = models.IntegerField()
    predicted_cured = models.IntegerField()
    predicted_death = models.IntegerField()
    confidence_score = models.FloatField(help_text="Confidence score (0-1)")
    prediction_date = models.DateTimeField(auto_now_add=True)
    input_data = models.JSONField(help_text="Input data used for prediction")
    
    class Meta:
        ordering = ['-prediction_date']
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"
    
    def __str__(self):
        return f"Prediction for {self.state_name} - {self.prediction_date.strftime('%Y-%m-%d %H:%M')}"

class ModelMetrics(models.Model):
    """Model to store ML model performance metrics"""
    model_name = models.CharField(max_length=100)
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    training_date = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=20)
    
    class Meta:
        ordering = ['-training_date']
        verbose_name = "Model Metrics"
        verbose_name_plural = "Model Metrics"
    
    def __str__(self):
        return f"{self.model_name} v{self.model_version} - {self.accuracy:.2%}"
