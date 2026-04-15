from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class SalesPrediction(models.Model):
    store = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(45)])
    department = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    is_holiday = models.BooleanField(default=False)
    temperature = models.FloatField(validators=[MinValueValidator(-50), MaxValueValidator(150)])
    cpi = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(500)])
    unemployment = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    size = models.IntegerField(validators=[MinValueValidator(30000), MaxValueValidator(250000)])
    week = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(52)])
    year = models.IntegerField(validators=[MinValueValidator(2010), MaxValueValidator(2030)])
    predicted_sales = models.FloatField(null=True, blank=True)
    model_used = models.CharField(max_length=50, default='ridge')
    confidence_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Store {self.store} - Dept {self.department} - Week {self.week}/{self.year}"
    
    class Meta:
        ordering = ['-created_at']
