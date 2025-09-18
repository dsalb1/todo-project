from django.conf import settings
from django.db import models
from django.utils import timezone

class ToDo(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='todos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
