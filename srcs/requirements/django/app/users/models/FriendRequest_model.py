import django
from django.db import models
from django.conf import settings
from users.models.User_model import CustomUser

django.setup()

class FriendRequest(models.Model):
  from_user = models.ForeignKey(
    CustomUser, related_name='from_user', on_delete=models.CASCADE
  )
  to_user = models.ForeignKey(
    CustomUser, related_name='to_user', on_delete=models.CASCADE
  )
