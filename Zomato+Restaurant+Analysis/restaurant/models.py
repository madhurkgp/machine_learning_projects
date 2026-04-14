from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class RestaurantPrediction(models.Model):
    """Model to store restaurant rating predictions"""
    
    # Input features
    online_order = models.BooleanField(default=False)
    book_table = models.BooleanField(default=False)
    votes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    location = models.CharField(max_length=100)
    rest_type = models.CharField(max_length=100)
    cuisines = models.CharField(max_length=200)
    approx_cost = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Prediction results
    predicted_rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        null=True, blank=True
    )
    model_used = models.CharField(max_length=50, default='RandomForest')
    confidence_score = models.FloatField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Restaurant Prediction"
        verbose_name_plural = "Restaurant Predictions"
    
    def __str__(self):
        return f"Prediction for {self.location} - {self.rest_type}"


class ModelMetrics(models.Model):
    """Model to store ML model performance metrics"""
    
    model_name = models.CharField(max_length=50)
    r2_score = models.FloatField()
    mean_squared_error = models.FloatField(null=True, blank=True)
    mean_absolute_error = models.FloatField(null=True, blank=True)
    training_samples = models.IntegerField(default=0)
    test_samples = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Model Metric"
        verbose_name_plural = "Model Metrics"
    
    def __str__(self):
        return f"{self.model_name} - R²: {self.r2_score:.3f}"
