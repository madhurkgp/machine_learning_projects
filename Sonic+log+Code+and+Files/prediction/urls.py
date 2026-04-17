from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.prediction_history, name='history'),
    path('detail/<int:prediction_id>/', views.prediction_detail, name='detail'),
    path('api/predict/', views.api_predict, name='api_predict'),
    path('sample/', views.sample_data, name='sample_data'),
    path('about/', views.about, name='about'),
]
