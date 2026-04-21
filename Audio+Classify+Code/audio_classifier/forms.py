from django import forms
from django.core.validators import FileExtensionValidator
from .models import AudioClassification


class AudioUploadForm(forms.ModelForm):
    """Form for uploading audio files for classification"""
    
    class Meta:
        model = AudioClassification
        fields = ['audio_file']
        widgets = {
            'audio_file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'accept': '.wav,.mp3,.flac,.m4a,.ogg',
                    'id': 'audio_file_input'
                }
            )
        }
        help_texts = {
            'audio_file': 'Upload an audio file (WAV, MP3, FLAC, M4A, OGG formats supported)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audio_file'].label = 'Audio File'
        self.fields['audio_file'].validators = [
            FileExtensionValidator(allowed_extensions=['wav', 'mp3', 'flac', 'm4a', 'ogg'])
        ]
    
    def clean_audio_file(self):
        """Validate the uploaded audio file"""
        audio_file = self.cleaned_data.get('audio_file')
        
        if audio_file:
            # Check file size (25MB limit)
            if audio_file.size > 25 * 1024 * 1024:
                raise forms.ValidationError(
                    'File size must be less than 25MB. Current size: {:.1f}MB'.format(
                        audio_file.size / (1024 * 1024)
                    )
                )
            
            # Check file extension
            allowed_extensions = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
            file_extension = audio_file.name.lower().split('.')[-1]
            
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError(
                    f'File type not supported. Allowed formats: {", ".join(allowed_extensions)}'
                )
        
        return audio_file


class SampleDataForm(forms.Form):
    """Form for selecting sample audio data"""
    
    SAMPLE_CHOICES = [
        ('dog_bark', 'Dog Bark'),
        ('car_horn', 'Car Horn'),
        ('street_music', 'Street Music'),
        ('air_conditioner', 'Air Conditioner'),
        ('drilling', 'Drilling'),
    ]
    
    sample_type = forms.ChoiceField(
        choices=SAMPLE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'sample_type_select'
            }
        ),
        help_text='Select a sample audio file for testing'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sample_type'].label = 'Sample Audio Type'
