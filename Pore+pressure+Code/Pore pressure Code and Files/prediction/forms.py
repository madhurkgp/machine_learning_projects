from django import forms

class PredictionForm(forms.Form):
    depth = forms.FloatField(
        label='Depth (m)',
        min_value=0,
        max_value=10000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter depth in meters',
            'step': '0.1'
        })
    )
    
    gr = forms.FloatField(
        label='Gamma Ray (GR)',
        min_value=0,
        max_value=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter GR value',
            'step': '0.1'
        })
    )
    
    rhob = forms.FloatField(
        label='Bulk Density (RHOB)',
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter RHOB value',
            'step': '0.01'
        })
    )
    
    vp = forms.FloatField(
        label='P-wave Velocity (Vp)',
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Vp value',
            'step': '0.01'
        })
    )
    
    vsh = forms.FloatField(
        label='Shale Volume (Vsh)',
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Vsh value',
            'step': '0.01'
        })
    )
    
    caliper = forms.FloatField(
        label='Caliper',
        min_value=0,
        max_value=20,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter caliper value',
            'step': '0.1'
        })
    )
    
    porosity = forms.FloatField(
        label='Porosity (%)',
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter porosity percentage',
            'step': '0.1'
        })
    )
    
    resistivity = forms.FloatField(
        label='Resistivity',
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter resistivity value',
            'step': '0.01'
        })
    )
    
    stress = forms.FloatField(
        label='Stress',
        min_value=0,
        max_value=10000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter stress value',
            'step': '1000'
        })
    )
