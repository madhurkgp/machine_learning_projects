from django import forms
from .models import RestaurantPrediction


class RestaurantPredictionForm(forms.ModelForm):
    """Form for restaurant rating prediction"""
    
    # Custom choices for dropdowns
    LOCATION_CHOICES = [
        ('BTM', 'BTM'),
        ('Banashankari', 'Banashankari'),
        ('Basavanagudi', 'Basavanagudi'),
        ('Jayanagar', 'Jayanagar'),
        ('Koramangala', 'Koramangala'),
        ('Indiranagar', 'Indiranagar'),
        ('Electronic City', 'Electronic City'),
        ('Marathahalli', 'Marathahalli'),
        ('Whitefield', 'Whitefield'),
        ('HSR Layout', 'HSR Layout'),
        ('Other', 'Other'),
    ]
    
    REST_TYPE_CHOICES = [
        ('Casual Dining', 'Casual Dining'),
        ('Quick Bites', 'Quick Bites'),
        ('Cafe', 'Cafe'),
        ('Delivery', 'Delivery'),
        ('Dessert Parlor', 'Dessert Parlor'),
        ('Bakery', 'Bakery'),
        ('Fine Dining', 'Fine Dining'),
        ('Bar', 'Bar'),
        ('Pub', 'Pub'),
        ('Lounge', 'Lounge'),
        ('Food Court', 'Food Court'),
        ('Other', 'Other'),
    ]
    
    CUISINES_CHOICES = [
        ('North Indian', 'North Indian'),
        ('South Indian', 'South Indian'),
        ('Chinese', 'Chinese'),
        ('Italian', 'Italian'),
        ('Continental', 'Continental'),
        ('Mexican', 'Mexican'),
        ('Thai', 'Thai'),
        ('Japanese', 'Japanese'),
        ('Arabian', 'Arabian'),
        ('Mughlai', 'Mughlai'),
        ('Biryani', 'Biryani'),
        ('Fast Food', 'Fast Food'),
        ('Cafe', 'Cafe'),
        ('Desserts', 'Desserts'),
        ('Beverages', 'Beverages'),
        ('Other', 'Other'),
    ]
    
    online_order = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    book_table = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    votes = forms.IntegerField(
        min_value=0,
        max_value=50000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of votes (0-50000)'
        })
    )
    
    location = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    rest_type = forms.ChoiceField(
        choices=REST_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    cuisines = forms.ChoiceField(
        choices=CUISINES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    approx_cost = forms.IntegerField(
        min_value=50,
        max_value=5000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Approximate cost for two people (50-5000)'
        })
    )
    
    class Meta:
        model = RestaurantPrediction
        fields = ['online_order', 'book_table', 'votes', 'location', 'rest_type', 'cuisines', 'approx_cost']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all form fields
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.Select)):
                field.widget.attrs.update({'class': 'form-control'})
        
        # Add help text
        self.fields['votes'].help_text = "Total number of ratings the restaurant has received"
        self.fields['location'].help_text = "Area/neighborhood where the restaurant is located"
        self.fields['rest_type'].help_text = "Type of restaurant establishment"
        self.fields['cuisines'].help_text = "Primary cuisine type served"
        self.fields['approx_cost'].help_text = "Average cost for two people in INR"
    
    def clean_votes(self):
        votes = self.cleaned_data.get('votes')
        if votes is not None and votes < 0:
            raise forms.ValidationError("Votes cannot be negative")
        return votes
    
    def clean_approx_cost(self):
        cost = self.cleaned_data.get('approx_cost')
        if cost is not None and cost < 50:
            raise forms.ValidationError("Minimum cost should be at least 50 INR")
        return cost
