from django.contrib import admin
from .models import AudioFile, AudioAnalysis

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'upload_date', 'duration', 'sample_rate', 'file_size']
    list_filter = ['upload_date', 'sample_rate']
    search_fields = ['name']
    readonly_fields = ['upload_date', 'duration', 'sample_rate']
    
    def file_size(self, obj):
        size = obj.audio_file.size
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    file_size.short_description = 'File Size'

@admin.register(AudioAnalysis)
class AudioAnalysisAdmin(admin.ModelAdmin):
    list_display = ['audio_file', 'analysis_date', 'zero_crossing_rate_avg', 'rms_energy_avg', 'spectral_centroid_avg']
    list_filter = ['analysis_date', 'frame_size', 'hop_length']
    search_fields = ['audio_file__name']
    readonly_fields = ['analysis_date', 'audio_file']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('audio_file', 'analysis_date', 'frame_size', 'hop_length')
        }),
        ('Time Domain Features', {
            'fields': ('amplitude_envelope_avg', 'zero_crossing_rate_avg', 'rms_energy_avg')
        }),
        ('Frequency Domain Features', {
            'fields': ('spectral_centroid_avg', 'spectral_bandwidth_avg', 'spectral_rolloff_avg')
        }),
        ('MFCC Features', {
            'fields': ('mfcc_features',)
        }),
    )
