from django.contrib import admin
from .models import SonicLogPrediction

@admin.register(SonicLogPrediction)
class SonicLogPredictionAdmin(admin.ModelAdmin):
    """
    Admin interface for Sonic Log Predictions
    """
    list_display = [
        'id', 'cal', 'cnc', 'gr', 'hrd', 'hrm', 'pe', 'zden',
        'dtc_predicted', 'dts_predicted', 'prediction_method', 'created_at'
    ]
    list_filter = ['prediction_method', 'created_at']
    search_fields = ['cal', 'cnc', 'gr']
    readonly_fields = ['dtc_predicted', 'dts_predicted', 'created_at']
    
    fieldsets = (
        ('Input Features', {
            'fields': ('cal', 'cnc', 'gr', 'hrd', 'hrm', 'pe', 'zden')
        }),
        ('Predictions', {
            'fields': ('dtc_predicted', 'dts_predicted', 'prediction_method'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Allow adding new predictions through admin
        return True
    
    def has_change_permission(self, request, obj=None):
        # Allow editing but not changing predictions
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
