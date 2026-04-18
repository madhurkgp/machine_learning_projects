from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('api/predict/', views.api_predict, name='api_predict'),
    path('api/sample/', views.get_sample_data, name='get_sample_data'),
]
