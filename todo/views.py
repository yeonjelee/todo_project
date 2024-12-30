from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import ToDo


# Render the home page
def home(request):
    return render(request, 'todo/home.html')


# Handle the main To-Do List functionality
@login_required
def todo_list(request):
    if request.method == 'POST':
        # Handle task addition
        if 'add_task' in request.POST:
            task_name = request.POST.get('task')
            if task_name:
                ToDo.objects.create(user=request.user, task=task_name)
                print(f"Task added: {task_name}")

        # Handle task editing
        if 'edit_task' in request.POST:
            task_id = request.POST.get('task_id')
            updated_task_name = request.POST.get('updated_task')
            if task_id and updated_task_name:
                task = get_object_or_404(ToDo, id=task_id, user=request.user)
                task.task = updated_task_name
                task.save()

        return redirect('todo_list')  # Redirect back to the task list after handling

    # Fetch incomplete and completed tasks
    incomplete_tasks = ToDo.objects.filter(user=request.user, is_completed=False)
    completed_tasks = ToDo.objects.filter(user=request.user, is_completed=True)

    # Redirect to the congrats page if all tasks are completed
    if not incomplete_tasks.exists() and completed_tasks.exists():
        ToDo.objects.filter(user=request.user).delete()
        return redirect('congrats_page')

    # Render the To-Do list template with tasks
    return render(request, 'todo/todo_list.html', {
        'tasks': incomplete_tasks,
        'completed_tasks': completed_tasks,
    })


# Toggle the completion status of a specific task
@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(ToDo, id=task_id, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    print(f"Task {task.id} status toggled to {task.is_completed}")
    return redirect('todo_list')


# Render the congratulation page
@login_required
def congrats_page(request):
    has_incomplete_tasks = ToDo.objects.filter(user=request.user, is_completed=False).exists()
    print(f"Incomplete tasks exist: {has_incomplete_tasks}")
    if has_incomplete_tasks:
        return redirect('todo_list')
    return render(request, 'todo/congrats.html', {'message': 'You completed all tasks!'})


# Handle user sign-up
def signup(request):
    if request.method == 'POST':
        print("POST request received:", request.POST)
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            print("Sign-up successful")
            return redirect('login')
        else:
            print("Form validation failed:", form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'todo/signup.html', {'form': form})


# Customize the login view
class CustomLoginView(LoginView):
    template_name = 'todo/login.html'

    def get_success_url(self):
        return '/todo'


# Delete all tasks for the logged-in user
@login_required
def delete_all_tasks(request):
    if request.method == 'POST':
        ToDo.objects.filter(user=request.user).delete()
        return redirect('todo_list')