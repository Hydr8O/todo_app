from django.urls import path
from auth_app import views

app_name='auth_app'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<slug:uid>/<slug:token>', views.activate, name='activate'),
]