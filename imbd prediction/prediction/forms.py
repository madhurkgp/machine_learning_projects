from django import forms

class MoviePredictionForm(forms.Form):
    """Form for collecting movie data for IMDB rating prediction"""
    
    # Numeric fields
    num_critic_for_reviews = forms.IntegerField(
        min_value=1, max_value=1000,
        initial=140,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of critic reviews'
        })
    )
    
    duration = forms.IntegerField(
        min_value=1, max_value=500,
        initial=107,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Duration in minutes'
        })
    )
    
    director_facebook_likes = forms.IntegerField(
        min_value=0, max_value=100000,
        initial=686,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Director Facebook likes'
        })
    )
    
    actor_3_facebook_likes = forms.IntegerField(
        min_value=0, max_value=100000,
        initial=645,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Third actor Facebook likes'
        })
    )
    
    actor_1_facebook_likes = forms.IntegerField(
        min_value=0, max_value=1000000,
        initial=6560,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Main actor Facebook likes'
        })
    )
    
    gross = forms.IntegerField(
        min_value=0,
        initial=48468410,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Gross revenue (USD)'
        })
    )
    
    num_voted_users = forms.IntegerField(
        min_value=0, max_value=2000000,
        initial=83668,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of voted users'
        })
    )
    
    cast_total_facebook_likes = forms.IntegerField(
        min_value=0, max_value=1000000,
        initial=9699,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Total cast Facebook likes'
        })
    )
    
    facenumber_in_poster = forms.IntegerField(
        min_value=0, max_value=50,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of faces in poster'
        })
    )
    
    num_user_for_reviews = forms.IntegerField(
        min_value=0, max_value=10000,
        initial=273,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of user reviews'
        })
    )
    
    budget = forms.IntegerField(
        min_value=0,
        initial=39752620,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Movie budget (USD)'
        })
    )
    
    title_year = forms.IntegerField(
        min_value=1900, max_value=2030,
        initial=2002,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Release year'
        })
    )
    
    actor_2_facebook_likes = forms.IntegerField(
        min_value=0, max_value=200000,
        initial=1652,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Second actor Facebook likes'
        })
    )
    
    aspect_ratio = forms.FloatField(
        min_value=0.5, max_value=5.0,
        initial=2.22,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Aspect ratio (e.g., 2.35)'
        })
    )
    
    movie_facebook_likes = forms.IntegerField(
        min_value=0, max_value=500000,
        initial=7526,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Movie Facebook likes'
        })
    )
    
    # Categorical fields
    COLOR_CHOICES = [
        ('Color', 'Color'),
        (' Black and White', 'Black and White'),
    ]
    
    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        initial='Color',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    CONTENT_RATING_CHOICES = [
        ('G', 'G - General Audiences'),
        ('PG', 'PG - Parental Guidance'),
        ('PG-13', 'PG-13 - Parents Strongly Cautioned'),
        ('R', 'R - Restricted'),
        ('NC-17', 'NC-17 - Adults Only'),
        ('Unrated', 'Unrated'),
        ('Approved', 'Approved'),
        ('Not Rated', 'Not Rated'),
        ('Passed', 'Passed'),
    ]
    
    content_rating = forms.ChoiceField(
        choices=CONTENT_RATING_CHOICES,
        initial='PG-13',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('French', 'French'),
        ('Spanish', 'Spanish'),
        ('Hindi', 'Hindi'),
        ('Mandarin', 'Mandarin'),
        ('German', 'German'),
        ('Japanese', 'Japanese'),
        ('Italian', 'Italian'),
        ('Cantonese', 'Cantonese'),
        ('Russian', 'Russian'),
        ('Portuguese', 'Portuguese'),
        ('Korean', 'Korean'),
    ]
    
    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        initial='English',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    COUNTRY_CHOICES = [
        ('USA', 'United States'),
        ('UK', 'United Kingdom'),
        ('France', 'France'),
        ('Germany', 'Germany'),
        ('Canada', 'Canada'),
        ('Australia', 'Australia'),
        ('India', 'India'),
        ('China', 'China'),
        ('Japan', 'Japan'),
        ('Spain', 'Spain'),
        ('Italy', 'Italy'),
        ('Russia', 'Russia'),
    ]
    
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        initial='USA',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
