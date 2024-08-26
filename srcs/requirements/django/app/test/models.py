from django.db import models

# Create your models here.
from django.conf import settings

class Test_User(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    alive = models.BooleanField(default=True)
    spectator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username