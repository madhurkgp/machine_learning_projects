from django import forms
from django.core.validators import FileExtensionValidator
from .models import AudioAnalysis


class AudioUploadForm(forms.ModelForm):
    """Form for uploading audio files for analysis"""
    
    class Meta:
        model = AudioAnalysis
        fields = ['audio_file']
        widgets = {
            'audio_file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'accept': '.wav,.mp3,.flac,.m4a,.ogg',
                    'id': 'audio_file'
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audio_file'].label = 'Select Audio File'
        self.fields['audio_file'].help_text = 'Supported formats: WAV, MP3, FLAC, M4A, OGG (Max size: 25MB)'
        self.fields['audio_file'].validators = [
            FileExtensionValidator(allowed_extensions=['wav', 'mp3', 'flac', 'm4a', 'ogg'])
        ]
    
    def clean_audio_file(self):
        """Validate audio file size and format"""
        audio_file = self.cleaned_data.get('audio_file')
        
        if audio_file:
            # Check file size (25MB limit)
            if audio_file.size > 25 * 1024 * 1024:
                raise forms.ValidationError('Audio file size must be less than 25MB.')
            
            # Check if file is actually audio (basic check)
            if not audio_file.content_type.startswith('audio/'):
                raise forms.ValidationError('Please upload a valid audio file.')
        
        return audio_file


class AudioAnalysisForm(forms.ModelForm):
    """Form for displaying and editing audio analysis results"""
    
    class Meta:
        model = AudioAnalysis
        fields = ['transcribed_text']
        widgets = {
            'transcribed_text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 8,
                    'placeholder': 'Transcribed text will appear here...'
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transcribed_text'].label = 'Transcribed Text'
        self.fields['transcribed_text'].widget.attrs['readonly'] = True
