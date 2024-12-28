from celery import shared_task
from .models import ToDo

@shared_task
def reset_todo_tasks():
    ToDo.objects.all().delete()
