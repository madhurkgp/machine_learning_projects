from django import forms

class PredictionForm(forms.Form):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    AGE_CHOICES = [
        ('0-17', '0-17'),
        ('18-25', '18-25'),
        ('26-35', '26-35'),
        ('36-45', '36-45'),
        ('46-50', '46-50'),
        ('51-55', '51-55'),
        ('55+', '55+'),
    ]
    
    CITY_CATEGORY_CHOICES = [
        ('A', 'Urban'),
        ('B', 'Suburban'),
        ('C', 'Rural'),
    ]
    
    STAY_YEARS_CHOICES = [
        ('0', 'Less than 1 year'),
        ('1', '1 year'),
        ('2', '2 years'),
        ('3', '3 years'),
        ('4', '4+ years'),
    ]
    
    OCCUPATION_CHOICES = [(i, f'Occupation {i}') for i in range(21)]  # 0-20
    
    # Basic user information
    user_id = forms.IntegerField(
        label='User ID',
        min_value=1000001,
        max_value=1006040,
        initial=1000001,
        help_text='Enter a user ID between 1000001 and 1006040'
    )
    
    product_id = forms.CharField(
        label='Product ID',
        max_length=10,
        initial='P00069042',
        help_text='Enter product ID (e.g., P00069042)'
    )
    
    # Demographics
    gender = forms.ChoiceField(
        label='Gender',
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    age = forms.ChoiceField(
        label='Age Group',
        choices=AGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    occupation = forms.ChoiceField(
        label='Occupation',
        choices=OCCUPATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    city_category = forms.ChoiceField(
        label='City Category',
        choices=CITY_CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    stay_years = forms.ChoiceField(
        label='Years in Current City',
        choices=STAY_YEARS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    marital_status = forms.ChoiceField(
        label='Marital Status',
        choices=[(0, 'Single'), (1, 'Married')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Product information
    product_category_1 = forms.IntegerField(
        label='Product Category 1',
        min_value=1,
        max_value=20,
        initial=1,
        help_text='Enter product category (1-20)'
    )
    
    product_category_2 = forms.FloatField(
        label='Product Category 2',
        min_value=2,
        max_value=18,
        required=False,
        help_text='Enter product category (2-18, optional)'
    )
    
    def clean_product_id(self):
        product_id = self.cleaned_data.get('product_id')
        if not product_id.startswith('P00'):
            product_id = 'P00' + product_id
        return product_id
    
    def clean_product_category_2(self):
        product_category_2 = self.cleaned_data.get('product_category_2')
        if product_category_2 is None or product_category_2 == '':
            return None
        return product_category_2
