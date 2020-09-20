from django.urls import path
from todo_app import views

app_name = 'todo_app'

urlpatterns = [
    path('current/', views.show_current_todos, name='current_todos'),
    path('completed/', views.show_completed_todos, name='completed_todos'),
    path('create/', views.create_todo, name='create_todo'),
    path('<int:todo_id>/edit/', views.update_todo, name='update_todo'),
    path('<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
    path('<int:todo_id>/complete/', views.complete_todo, name='complete_todo'),
]