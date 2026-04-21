from django.urls import path
from . import views

app_name = 'audio_classifier'

urlpatterns = [
    path('', views.home, name='home'),
    path('result/<int:pk>/', views.classification_result, name='classification_result'),
    path('history/', views.classification_history, name='classification_history'),
    path('sample-data/', views.sample_data, name='sample_data'),
    path('api/classify/', views.classify_audio_api, name='classify_audio_api'),
    path('download/<int:pk>/', views.download_results, name='download_results'),
]
