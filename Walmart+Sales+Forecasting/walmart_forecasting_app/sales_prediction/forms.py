from django import forms
from .models import SalesPrediction

class SalesPredictionForm(forms.ModelForm):
    class Meta:
        model = SalesPrediction
        fields = ['store', 'department', 'is_holiday', 'temperature', 'cpi', 
                 'unemployment', 'size', 'week', 'year']
        widgets = {
            'store': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter store number (1-45)',
                'min': '1',
                'max': '45'
            }),
            'department': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter department number (1-99)',
                'min': '1',
                'max': '99'
            }),
            'is_holiday': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter temperature (-50 to 150)',
                'step': '0.1',
                'min': '-50',
                'max': '150'
            }),
            'cpi': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Consumer Price Index (0-500)',
                'step': '0.01',
                'min': '0',
                'max': '500'
            }),
            'unemployment': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter unemployment rate (0-50)',
                'step': '0.1',
                'min': '0',
                'max': '50'
            }),
            'size': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter store size (30000-250000)',
                'min': '30000',
                'max': '250000'
            }),
            'week': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter week number (1-52)',
                'min': '1',
                'max': '52'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter year (2010-2030)',
                'min': '2010',
                'max': '2030'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['store'].label = 'Store Number'
        self.fields['department'].label = 'Department Number'
        self.fields['is_holiday'].label = 'Holiday Week'
        self.fields['temperature'].label = 'Temperature (°F)'
        self.fields['cpi'].label = 'Consumer Price Index'
        self.fields['unemployment'].label = 'Unemployment Rate (%)'
        self.fields['size'].label = 'Store Size (sq ft)'
        self.fields['week'].label = 'Week Number'
        self.fields['year'].label = 'Year'
