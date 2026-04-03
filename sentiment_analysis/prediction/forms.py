from django import forms

class SentimentAnalysisForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter your text here for sentiment analysis...',
                'id': 'text-input'
            }
        ),
        label='Text to Analyze',
        min_length=1,
        max_length=5000,
        error_messages={
            'required': 'Please enter some text to analyze.',
            'min_length': 'Text must be at least 1 character long.',
            'max_length': 'Text cannot exceed 5000 characters.'
        }
    )

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text or not text.strip():
            raise forms.ValidationError('Please enter valid text to analyze.')
        return text.strip()
