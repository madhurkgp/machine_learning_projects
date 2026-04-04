from django import forms
import numpy as np

class ParkinsonPredictionForm(forms.Form):
    # MDVP Fo (Hz) - Average vocal fundamental frequency
    mdvp_fo = forms.FloatField(
        label='Average Vocal Fundamental Frequency (Hz)',
        min_value=50,
        max_value=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 154.23',
            'step': '0.001'
        })
    )
    
    # MDVP Fhi (Hz) - Maximum vocal fundamental frequency
    mdvp_fhi = forms.FloatField(
        label='Maximum Vocal Fundamental Frequency (Hz)',
        min_value=50,
        max_value=600,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 197.10',
            'step': '0.001'
        })
    )
    
    # MDVP Flo (Hz) - Minimum vocal fundamental frequency
    mdvp_flo = forms.FloatField(
        label='Minimum Vocal Fundamental Frequency (Hz)',
        min_value=50,
        max_value=250,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 116.32',
            'step': '0.001'
        })
    )
    
    # Jitter measures
    mdvp_jitter = forms.FloatField(
        label='MDVP Jitter (%)',
        min_value=0,
        max_value=0.05,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.006',
            'step': '0.00001'
        })
    )
    
    mdvp_jitter_abs = forms.FloatField(
        label='MDVP Jitter (Absolute)',
        min_value=0,
        max_value=0.0003,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.00004',
            'step': '0.000001'
        })
    )
    
    mdvp_rap = forms.FloatField(
        label='MDVP RAP',
        min_value=0,
        max_value=0.025,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.003',
            'step': '0.00001'
        })
    )
    
    mdvp_ppq = forms.FloatField(
        label='MDVP PPQ',
        min_value=0,
        max_value=0.025,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.003',
            'step': '0.00001'
        })
    )
    
    jitter_ddp = forms.FloatField(
        label='Jitter DDP',
        min_value=0,
        max_value=0.07,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.009',
            'step': '0.00001'
        })
    )
    
    # Shimmer measures
    mdvp_shimmer = forms.FloatField(
        label='MDVP Shimmer',
        min_value=0,
        max_value=0.15,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.029',
            'step': '0.00001'
        })
    )
    
    mdvp_shimmer_db = forms.FloatField(
        label='MDVP Shimmer (dB)',
        min_value=0,
        max_value=1.5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.282',
            'step': '0.001'
        })
    )
    
    shimmer_apq3 = forms.FloatField(
        label='Shimmer APQ3',
        min_value=0,
        max_value=0.05,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.016',
            'step': '0.00001'
        })
    )
    
    shimmer_apq5 = forms.FloatField(
        label='Shimmer APQ5',
        min_value=0,
        max_value=0.08,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.017',
            'step': '0.00001'
        })
    )
    
    mdvp_apq = forms.FloatField(
        label='MDVP APQ',
        min_value=0,
        max_value=0.08,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.016',
            'step': '0.00001'
        })
    )
    
    shimmer_dda = forms.FloatField(
        label='Shimmer DDA',
        min_value=0,
        max_value=0.2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.046',
            'step': '0.00001'
        })
    )
    
    # Noise measures
    nhr = forms.FloatField(
        label='NHR (Noise to Harmonic Ratio)',
        min_value=0,
        max_value=0.35,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.024',
            'step': '0.00001'
        })
    )
    
    hnr = forms.FloatField(
        label='HNR (Harmonic to Noise Ratio)',
        min_value=5,
        max_value=40,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 21.88',
            'step': '0.001'
        })
    )
    
    # Nonlinear measures
    rpde = forms.FloatField(
        label='RPDE (Recurrence Period Density Entropy)',
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.498',
            'step': '0.001'
        })
    )
    
    dfa = forms.FloatField(
        label='DFA (Detrended Fluctuation Analysis)',
        min_value=0.5,
        max_value=0.9,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.718',
            'step': '0.001'
        })
    )
    
    spread1 = forms.FloatField(
        label='Spread1',
        min_value=-8,
        max_value=-2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., -5.684',
            'step': '0.001'
        })
    )
    
    spread2 = forms.FloatField(
        label='Spread2',
        min_value=0,
        max_value=0.5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.226',
            'step': '0.001'
        })
    )
    
    d2 = forms.FloatField(
        label='D2',
        min_value=1,
        max_value=4,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 2.381',
            'step': '0.001'
        })
    )
    
    ppe = forms.FloatField(
        label='PPE (Pitch Period Entropy)',
        min_value=0,
        max_value=0.6,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.206',
            'step': '0.001'
        })
    )

    def get_features_array(self):
        """Return form data as numpy array in the correct order for the model"""
        return np.array([
            self.cleaned_data['mdvp_fo'],
            self.cleaned_data['mdvp_fhi'],
            self.cleaned_data['mdvp_flo'],
            self.cleaned_data['mdvp_jitter'],
            self.cleaned_data['mdvp_jitter_abs'],
            self.cleaned_data['mdvp_rap'],
            self.cleaned_data['mdvp_ppq'],
            self.cleaned_data['jitter_ddp'],
            self.cleaned_data['mdvp_shimmer'],
            self.cleaned_data['mdvp_shimmer_db'],
            self.cleaned_data['shimmer_apq3'],
            self.cleaned_data['shimmer_apq5'],
            self.cleaned_data['mdvp_apq'],
            self.cleaned_data['shimmer_dda'],
            self.cleaned_data['nhr'],
            self.cleaned_data['hnr'],
            self.cleaned_data['rpde'],
            self.cleaned_data['dfa'],
            self.cleaned_data['spread1'],
            self.cleaned_data['spread2'],
            self.cleaned_data['d2'],
            self.cleaned_data['ppe']
        ]).reshape(1, -1)
