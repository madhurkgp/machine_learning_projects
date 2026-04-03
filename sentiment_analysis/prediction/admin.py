from django.contrib import admin
from .models import SentimentPrediction

@admin.register(SentimentPrediction)
class SentimentPredictionAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'prediction', 'confidence', 'created_at']
    list_filter = ['prediction', 'created_at']
    search_fields = ['text']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Text'
