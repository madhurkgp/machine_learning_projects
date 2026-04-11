from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_churn, name='predict_churn'),
    path('sample-data/', views.get_sample_data, name='get_sample_data'),
]
