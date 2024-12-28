from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('todo/congrats/', views.congrats_page, name='congrats_page'),
    path('signup/', views.signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/todo/'), name='logout'),
    path('todo/delete_all/', views.delete_all_tasks, name='delete_all_tasks'),
]
