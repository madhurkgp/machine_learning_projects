from django.contrib import admin
from .models import SalesPrediction

@admin.register(SalesPrediction)
class SalesPredictionAdmin(admin.ModelAdmin):
    list_display = ['store', 'department', 'week', 'year', 'predicted_sales', 
                   'confidence_score', 'created_at']
    list_filter = ['store', 'department', 'is_holiday', 'year', 'created_at']
    search_fields = ['store', 'department']
    readonly_fields = ['predicted_sales', 'confidence_score', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Input Parameters', {
            'fields': ('store', 'department', 'is_holiday', 'temperature', 
                      'cpi', 'unemployment', 'size', 'week', 'year')
        }),
        ('Prediction Results', {
            'fields': ('predicted_sales', 'confidence_score', 'model_used'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
