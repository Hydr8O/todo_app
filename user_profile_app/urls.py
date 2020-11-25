from django.urls import path
from user_profile_app import views

app_name = 'user_profile_app'

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('clear_statistics', views.clear_statistics, name='clear_statistics'),
]