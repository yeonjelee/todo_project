from django.db import models
from django.contrib.auth.models import User

# ToDo model to manage user tasks
class ToDo(models.Model):
    # Foreign key to link each task to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Task description
    task = models.CharField(max_length=300)

    # Status to check if the task is completed
    is_completed = models.BooleanField(default=False)

    # Date when the task was created (auto-filled when created)
    date = models.DateField(auto_now_add=True)

    # String representation of the task (for admin display or debugging)
    def __str__(self):
        return f"{self.task}"