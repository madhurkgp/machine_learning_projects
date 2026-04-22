from django.contrib import admin
from .models import VoiceInteraction, VoiceCommand


@admin.register(VoiceInteraction)
class VoiceInteractionAdmin(admin.ModelAdmin):
    list_display = ['transcribed_text', 'command_type', 'is_successful', 'created_at']
    list_filter = ['command_type', 'is_successful', 'created_at']
    search_fields = ['transcribed_text', 'response_text', 'action_taken']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Command Information', {
            'fields': ('voice_command', 'transcribed_text', 'command_type')
        }),
        ('Response Information', {
            'fields': ('response_text', 'action_taken', 'is_successful')
        }),
        ('Technical Details', {
            'fields': ('confidence_score', 'response_time_ms', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VoiceCommand)
class VoiceCommandAdmin(admin.ModelAdmin):
    list_display = ['command_type', 'description', 'is_active', 'usage_count', 'created_at']
    list_filter = ['command_type', 'is_active', 'created_at']
    search_fields = ['trigger_phrases', 'description', 'action_url']
    readonly_fields = ['created_at', 'usage_count']
    ordering = ['command_type']
    
    fieldsets = (
        ('Command Configuration', {
            'fields': ('trigger_phrases', 'command_type', 'description')
        }),
        ('Action Configuration', {
            'fields': ('action_url', 'is_active')
        }),
        ('Statistics', {
            'fields': ('usage_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )
