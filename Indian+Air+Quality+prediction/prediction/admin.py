from django.contrib import admin
from .models import AirQualityPrediction

@admin.register(AirQualityPrediction)
class AirQualityPredictionAdmin(admin.ModelAdmin):
    list_display = ['so2', 'no2', 'rspm', 'spm', 'aqi_value', 'aqi_category', 'created_at']
    list_filter = ['aqi_category', 'created_at']
    search_fields = ['aqi_category']
    readonly_fields = ['aqi_value', 'aqi_category', 'created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False  # Only allow predictions through the form
