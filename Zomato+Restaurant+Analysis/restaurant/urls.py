from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.home, name='home'),
    path('result/<int:pk>/', views.prediction_result, name='prediction_result'),
    path('history/', views.predictions_history, name='history'),
    path('analytics/', views.analytics, name='analytics'),
    path('api/predict/', views.predict_api, name='predict_api'),
    path('load-sample/', views.load_sample_data, name='load_sample_data'),
]
