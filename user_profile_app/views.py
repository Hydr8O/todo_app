from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from todo_app.models import Todo

def __get_user_statistics(user):
    average_per_day = Todo.objects.get_average_per_day(user)
    n_completed_todos = Todo.objects.get_n_completed(user)
    n_completed_today = Todo.objects.get_n_completed_by_date(
        user, 
        timezone.localdate()
    )

    if average_per_day == int(average_per_day):
        average_per_day = int(average_per_day)
    
    return {
        'average_per_day': average_per_day,
        'n_completed_todos': n_completed_todos,
        'n_completed_today': n_completed_today
    }

@login_required
def user_profile(request):
    user_statistics = __get_user_statistics(request.user)
    n_completed_todos = user_statistics.get('n_completed_todos')
    average_per_day = user_statistics.get('average_per_day')
    n_completed_today = user_statistics.get('n_completed_today')

    return render(
        request,
        'user_profile_app/user_profile.html',
        {
            'n_completed_todos': n_completed_todos,
            'n_completed_today': n_completed_today,
            'average_per_day': average_per_day
        }
    )

@login_required
def clear_statistics(request):
    if request.method == 'POST':
        todos = Todo.objects.filter(
            user=request.user, 
            completed_at__isnull=False
        )
        todos.delete()
        messages.info(request, 'Your statistics have been cleared')
        return redirect('user_profile_app:user_profile')
