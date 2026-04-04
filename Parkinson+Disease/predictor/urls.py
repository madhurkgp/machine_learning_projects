from django.urls import path
from . import views

app_name = 'predictor'

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('sample-data/', views.sample_data, name='sample_data'),
    path('about/', views.about, name='about'),
]
