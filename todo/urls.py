from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # To-Do List page (main)
    path('todo/', views.todo_list, name='todo_list'),

    # Toggle task completion status
    path('todo/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),

    # Congratulations page
    path('todo/congrats/', views.congrats_page, name='congrats_page'),

    # User signup page
    path('signup/', views.signup, name='signup'),

    # User login page (customized view)
    path('login/', CustomLoginView.as_view(), name='login'),

    # User logout with redirection to To-Do List page
    path('logout/', LogoutView.as_view(next_page='/todo/'), name='logout'),

    # Delete all tasks for the current user
    path('todo/delete_all/', views.delete_all_tasks, name='delete_all_tasks'),
]

