from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/predict/', views.api_predict, name='api_predict'),
    path('history/', views.history, name='history'),
    path('api/samples/', views.sample_texts, name='sample_texts'),
]
