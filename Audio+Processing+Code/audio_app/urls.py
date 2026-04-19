from django.urls import path
from . import views

app_name = 'audio_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_audio, name='upload_audio'),
    path('analyze/', views.analyze_audio, name='analyze_audio'),
    path('results/<int:analysis_id>/', views.analysis_results, name='analysis_results'),
    path('load-sample/', views.load_sample_data, name='load_sample_data'),
]
