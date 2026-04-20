from django.urls import path
from . import views

app_name = 'speech_analyzer'

urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/<int:pk>/', views.analyze_audio, name='analyze_audio'),
    path('results/<int:pk>/', views.analysis_results, name='analysis_results'),
    path('history/', views.history, name='history'),
    path('delete/<int:pk>/', views.delete_analysis, name='delete_analysis'),
    path('sample-data/', views.sample_data, name='sample_data'),
]
