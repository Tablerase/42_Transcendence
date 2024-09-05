from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
  total_wins = models.IntegerField(default=0)
  total_losses = models.IntegerField(default=0)
  friends = models.ManyToManyField("CustomUser", blank=True)
  blocked_users = models.ManyToManyField("CustomUser", blank=True, related_name="blocked_by")
  last_online = models.DateTimeField(blank=True, null=True)
  
  def __str__(self):
    return self.username
  
  def is_online(self):
    return self.last_online and (timezone.now() - self.last_online) < timezone.timedelta(minutes=15)

  def get_online_info(self):
    if self.is_online():
        return _('Online')
    if self.last_online:
        return _('Last visit {}').format(naturaltime(self.last_online))
    return _('Unknown')
