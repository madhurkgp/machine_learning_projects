from django.db import models
from django.utils import timezone


class VoiceInteraction(models.Model):
    """Model to store voice assistant interactions"""
    
    COMMAND_TYPES = [
        ('wikipedia', 'Wikipedia Search'),
        ('web_open', 'Open Website'),
        ('time_query', 'Time Query'),
        ('greeting', 'Greeting'),
        ('unknown', 'Unknown Command'),
        ('error', 'Error'),
    ]
    
    voice_command = models.TextField(help_text="The voice command as spoken by user")
    transcribed_text = models.TextField(help_text="Text transcribed from speech")
    command_type = models.CharField(max_length=20, choices=COMMAND_TYPES, default='unknown')
    response_text = models.TextField(help_text="Assistant's response")
    action_taken = models.TextField(blank=True, help_text="Action performed by assistant")
    confidence_score = models.FloatField(null=True, blank=True, help_text="Speech recognition confidence")
    response_time_ms = models.IntegerField(null=True, blank=True, help_text="Response time in milliseconds")
    created_at = models.DateTimeField(default=timezone.now)
    is_successful = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Voice Interaction"
        verbose_name_plural = "Voice Interactions"
    
    def __str__(self):
        return f"{self.voice_command[:50]}... - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class VoiceCommand(models.Model):
    """Model to store predefined voice commands"""
    
    trigger_phrases = models.TextField(help_text="Comma-separated trigger phrases")
    command_type = models.CharField(max_length=20, choices=VoiceInteraction.COMMAND_TYPES)
    action_url = models.URLField(blank=True, help_text="URL to open for web commands")
    description = models.TextField(help_text="Description of what this command does")
    is_active = models.BooleanField(default=True)
    usage_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['command_type']
        verbose_name = "Voice Command"
        verbose_name_plural = "Voice Commands"
    
    def __str__(self):
        return f"{self.command_type}: {self.trigger_phrases[:30]}..."
    
    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])
