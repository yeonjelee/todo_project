from django.db import models
from django.contrib.auth.models import User

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=300)
    is_completed = models.BooleanField (default = False) # 할 일 마쳤는지 체크
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.task}"