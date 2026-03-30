from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/predict/', views.api_predict, name='api_predict'),
    path('sample-data/', views.sample_data, name='sample_data'),
    path('about/', views.about, name='about'),
]
