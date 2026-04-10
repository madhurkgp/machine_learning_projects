from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.prediction_form, name='prediction_form'),
    path('api/predict/', views.api_predict, name='api_predict'),
    path('visualization/', views.data_visualization, name='visualization'),
    path('history/', views.predictions_history, name='history'),
    path('model-info/', views.model_info, name='model_info'),
    path('load-sample-data/', views.load_sample_data, name='load_sample_data'),
]
