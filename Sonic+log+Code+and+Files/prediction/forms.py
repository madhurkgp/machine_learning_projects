from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import SonicLogPrediction

class SonicLogPredictionForm(forms.ModelForm):
    """
    Form for sonic log prediction input
    """
    
    class Meta:
        model = SonicLogPrediction
        fields = ['cal', 'cnc', 'gr', 'hrd', 'hrm', 'pe', 'zden']
        widgets = {
            'cal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'placeholder': 'e.g., 8.5781'
            }),
            'cnc': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'placeholder': 'e.g., 0.3521'
            }),
            'gr': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'placeholder': 'e.g., 55.1824'
            }),
            'hrd': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'placeholder': 'e.g., 0.8121'
            }),
            'hrm': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'placeholder': 'e.g., 0.7810'
            }),
            'pe': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'placeholder': 'e.g., 6.8291'
            }),
            'zden': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'placeholder': 'e.g., 2.3256'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cal'].label = 'Caliper (Inch)'
        self.fields['cnc'].label = 'Neutron (dec)'
        self.fields['gr'].label = 'Gamma Ray (API)'
        self.fields['hrd'].label = 'Deep Resistivity (Ohm/m)'
        self.fields['hrm'].label = 'Medium Resistivity (Ohm/m)'
        self.fields['pe'].label = 'Photo-electric Factor (Barn)'
        self.fields['zden'].label = 'Density (g/m³)'
        
        # Add help text
        self.fields['cal'].help_text = 'Caliper measurement in inches (typically 6-12)'
        self.fields['cnc'].help_text = 'Neutron log in decimal units (typically 0-0.7)'
        self.fields['gr'].help_text = 'Gamma Ray log in API units (typically 0-250)'
        self.fields['hrd'].help_text = 'Deep resistivity in Ohm per meter'
        self.fields['hrm'].help_text = 'Medium resistivity in Ohm per meter'
        self.fields['pe'].help_text = 'Photo-electric factor in Barn (typically 1-10)'
        self.fields['zden'].help_text = 'Density in grams per cubic meter (typically 2-3)'
    
    def clean_cal(self):
        cal = self.cleaned_data.get('cal')
        if cal and (cal < 6 or cal > 12):
            raise forms.ValidationError('Caliper value should be between 6 and 12 inches.')
        return cal
    
    def clean_cnc(self):
        cnc = self.cleaned_data.get('cnc')
        if cnc and (cnc < 0 or cnc > 0.7):
            raise forms.ValidationError('Neutron log value should be between 0 and 0.7.')
        return cnc
    
    def clean_gr(self):
        gr = self.cleaned_data.get('gr')
        if gr and (gr < 0 or gr > 250):
            raise forms.ValidationError('Gamma Ray value should be between 0 and 250 API.')
        return gr
    
    def clean_pe(self):
        pe = self.cleaned_data.get('pe')
        if pe and (pe < 1 or pe > 10):
            raise forms.ValidationError('Photo-electric factor should be between 1 and 10 Barn.')
        return pe
    
    def clean_zden(self):
        zden = self.cleaned_data.get('zden')
        if zden and (zden < 2 or zden > 3):
            raise forms.ValidationError('Density should be between 2 and 3 g/m³.')
        return zden
