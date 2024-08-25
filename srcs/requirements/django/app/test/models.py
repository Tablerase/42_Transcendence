from django.db import models

# Create your models here.
from django.conf import settings

class Test_User(models.Model):
    username = models.CharField(max_length=100)
    alive = models.BooleanField(default=True)
    spectator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username