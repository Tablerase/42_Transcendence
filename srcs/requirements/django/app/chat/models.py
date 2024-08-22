from django.db import models
from django.utils import timezone
from django.conf import settings

class Comment(models.Model):
  content = models.CharField(max_length=160)
  time = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.content
