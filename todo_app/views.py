from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.decorators import login_required
from todo_app.models import Todo


@login_required
def show_current_todos(request):
    todos = Todo.objects.filter(user=request.user, completed_at__isnull=True)
    if len(todos) == 0:
        messages.info(request, 'You don\'t have current todos')
    return render(
        request,
        'todo_app/current_todos.html',
        {'todos': todos}
    )

@login_required
def show_completed_todos(request):
    date = request.GET.get('date')
    if not date:
        date = timezone.localdate()
    todos = Todo.objects.get_completed_by_date(request.user, date)
    if len(todos) == 0:
        messages.info(request, 'You haven\t completed any todos on this day')
    return render(
        request,
        'todo_app/completed_todos.html',
        {
            'todos': todos,
            'current_date': timezone.localdate()
        }
    )

@login_required
def create_todo(request):
    if request.method == "POST":
        title = request.POST.get('title')
        memo = request.POST.get('memo')
        Todo.objects.create(
            title=title,
            memo=memo,
            user=request.user
        )
        messages.success(request, f'Todo "{title}" has been created')
        return redirect('todo_app:create_todo')
    else:    
        return render(
            request,
            'todo_app/create_todo.html'
        )

@login_required
def update_todo(request, todo_id):
    if request.method == "POST":
        new_title = request.POST.get('title')
        new_memo = request.POST.get('memo')
        todo_to_update = get_object_or_404(Todo, pk=todo_id)
        todo_to_update.title = new_title
        todo_to_update.memo = new_memo
        todo_to_update.save()
        return redirect('todo_app:current_todos')
    else:
        todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    return render(
        request,
        'todo_app/update_todo.html',
        {'todo': todo}
    )

@login_required
def delete_todo(request, todo_id):
    if request.method == "POST":
        todo_to_delete = get_object_or_404(Todo, pk=todo_id, user=request.user)
        todo_to_delete.delete()
        messages.success(request, f'Todo "{todo_to_delete.title}" has been deleted')
        if todo_to_delete.completed_at:
            return redirect('todo_app:completed_todos')
        else:
            return redirect('todo_app:current_todos')
    else:
        raise Http404

@login_required
def complete_todo(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.completed_at = timezone.now()
        todo.save()
        return redirect('todo_app:current_todos')
    else:
        raise Http404