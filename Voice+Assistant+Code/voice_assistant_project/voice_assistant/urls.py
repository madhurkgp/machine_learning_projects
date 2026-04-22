from django.urls import path
from . import views

app_name = 'voice_assistant'

urlpatterns = [
    path('', views.home, name='home'),
    path('process-command/', views.process_voice_command, name='process_command'),
    path('test-microphone/', views.test_microphone, name='test_microphone'),
    path('history/', views.command_history, name='command_history'),
    path('analytics/', views.analytics, name='analytics'),
    path('clear-history/', views.clear_history, name='clear_history'),
    path('help/', views.help_page, name='help'),
]
