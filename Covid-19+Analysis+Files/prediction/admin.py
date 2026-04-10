from django.contrib import admin
from .models import CovidData, Prediction, ModelMetrics

@admin.register(CovidData)
class CovidDataAdmin(admin.ModelAdmin):
    list_display = ['state_name', 'active_cases', 'positive_cases', 'cured_cases', 'death_cases', 'date_recorded', 'recovery_rate', 'death_rate']
    list_filter = ['state_name', 'date_recorded']
    search_fields = ['state_name']
    readonly_fields = ['date_recorded', 'recovery_rate', 'death_rate', 'active_rate']
    ordering = ['-date_recorded']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('state_name', 'state_code', 'date_recorded')
        }),
        ('Current Cases', {
            'fields': ('active_cases', 'positive_cases', 'cured_cases', 'death_cases')
        }),
        ('New Cases', {
            'fields': ('new_active', 'new_positive', 'new_cured', 'new_death')
        }),
        ('Calculated Rates', {
            'fields': ('recovery_rate', 'death_rate', 'active_rate'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['state_name', 'predicted_active', 'predicted_positive', 'predicted_cured', 'predicted_death', 'confidence_score', 'prediction_date', 'user']
    list_filter = ['state_name', 'prediction_date', 'confidence_score']
    search_fields = ['state_name', 'user__username']
    readonly_fields = ['prediction_date', 'input_data']
    ordering = ['-prediction_date']
    
    fieldsets = (
        ('Prediction Information', {
            'fields': ('user', 'state_name', 'prediction_date', 'confidence_score')
        }),
        ('Predicted Values', {
            'fields': ('predicted_active', 'predicted_positive', 'predicted_cured', 'predicted_death')
        }),
        ('Input Data', {
            'fields': ('input_data',),
            'classes': ('collapse',)
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Allow superusers to delete predictions
        return request.user.is_superuser

@admin.register(ModelMetrics)
class ModelMetricsAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'model_version', 'accuracy', 'precision', 'recall', 'f1_score', 'training_date']
    list_filter = ['model_name', 'training_date']
    search_fields = ['model_name', 'model_version']
    readonly_fields = ['training_date']
    ordering = ['-training_date']
    
    fieldsets = (
        ('Model Information', {
            'fields': ('model_name', 'model_version', 'training_date')
        }),
        ('Performance Metrics', {
            'fields': ('accuracy', 'precision', 'recall', 'f1_score')
        }),
    )
