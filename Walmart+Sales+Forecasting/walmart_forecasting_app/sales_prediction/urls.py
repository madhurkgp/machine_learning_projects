from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_sales, name='predict_sales'),
    path('result/<int:pk>/', views.prediction_result, name='prediction_result'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('sample-data/', views.sample_data, name='sample_data'),
    path('api/predict/', views.api_predict, name='api_predict'),
]
