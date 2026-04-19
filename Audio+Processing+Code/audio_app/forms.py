from django import forms
from .models import AudioFile

class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['name', 'audio_file']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a name for your audio file',
                'required': True
            }),
            'audio_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.wav,.mp3,.flac,.m4a,.ogg',
                'required': True
            }),
        }
    
    def clean_audio_file(self):
        audio_file = self.cleaned_data.get('audio_file')
        
        if audio_file:
            # Check file size (max 50MB)
            if audio_file.size > 50 * 1024 * 1024:
                raise forms.ValidationError("Audio file size must be less than 50MB.")
            
            # Check file extension
            allowed_extensions = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
            file_extension = audio_file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError(
                    "Unsupported file format. Please upload WAV, MP3, FLAC, M4A, or OGG files."
                )
        
        return audio_file
