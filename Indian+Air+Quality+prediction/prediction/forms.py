from django import forms
from .models import AirQualityPrediction

class AirQualityPredictionForm(forms.ModelForm):
    class Meta:
        model = AirQualityPrediction
        fields = ['so2', 'no2', 'rspm', 'spm']
        widgets = {
            'so2': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter SO2 value (µg/m³)',
                'min': '0',
                'step': '0.1',
                'required': True
            }),
            'no2': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter NO2 value (µg/m³)',
                'min': '0',
                'step': '0.1',
                'required': True
            }),
            'rspm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter RSPM value (µg/m³)',
                'min': '0',
                'step': '0.1',
                'required': True
            }),
            'spm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter SPM value (µg/m³)',
                'min': '0',
                'step': '0.1',
                'required': True
            }),
        }
    
    def clean_so2(self):
        so2 = self.cleaned_data.get('so2')
        if so2 is None or so2 < 0:
            raise forms.ValidationError("SO2 value must be a positive number.")
        return so2
    
    def clean_no2(self):
        no2 = self.cleaned_data.get('no2')
        if no2 is None or no2 < 0:
            raise forms.ValidationError("NO2 value must be a positive number.")
        return no2
    
    def clean_rspm(self):
        rspm = self.cleaned_data.get('rspm')
        if rspm is None or rspm < 0:
            raise forms.ValidationError("RSPM value must be a positive number.")
        return rspm
    
    def clean_spm(self):
        spm = self.cleaned_data.get('spm')
        if spm is None or spm < 0:
            raise forms.ValidationError("SPM value must be a positive number.")
        return spm
