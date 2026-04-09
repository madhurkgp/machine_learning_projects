from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('', views.home, name='home'),
    path('sample-data/', views.sample_data, name='sample_data'),
    path('api/predict/', views.predict_api, name='predict_api'),
]
