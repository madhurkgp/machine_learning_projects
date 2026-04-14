from django.contrib import admin
from .models import RestaurantPrediction, ModelMetrics


@admin.register(RestaurantPrediction)
class RestaurantPredictionAdmin(admin.ModelAdmin):
    list_display = [
        'location', 'rest_type', 'cuisines', 'predicted_rating', 
        'model_used', 'confidence_score', 'created_at'
    ]
    list_filter = [
        'model_used', 'online_order', 'book_table', 'location', 'rest_type'
    ]
    search_fields = ['location', 'rest_type', 'cuisines']
    readonly_fields = ['created_at', 'ip_address']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Input Features', {
            'fields': ('online_order', 'book_table', 'votes', 'location', 'rest_type', 'cuisines', 'approx_cost')
        }),
        ('Prediction Results', {
            'fields': ('predicted_rating', 'model_used', 'confidence_score')
        }),
        ('Metadata', {
            'fields': ('created_at', 'ip_address'),
            'classes': ('collapse',)
        })
    )


@admin.register(ModelMetrics)
class ModelMetricsAdmin(admin.ModelAdmin):
    list_display = [
        'model_name', 'r2_score', 'mean_squared_error', 
        'mean_absolute_error', 'training_samples', 'test_samples', 'created_at'
    ]
    readonly_fields = ['created_at']
    ordering = ['-r2_score']
