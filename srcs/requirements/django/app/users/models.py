from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  image = models.ImageField(default='default.jpg', upload_to='profile_pics')

  def __str__(self):
    return f'{self.user.username} Profile'

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    if self.image:
      img_path = self.image.path
      img = Image.open(img_path)

      if img.height != img.width:
        min_dimension = min(img.height, img.width)
        left = (img.width - min_dimension) / 2
        top = (img.height - min_dimension) / 2
        right = (img.width + min_dimension) / 2
        bottom = (img.height + min_dimension) / 2
        img = img.crop((left, top, right, bottom))

      if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)

      img.save(img_path)

class CustomUser(AbstractUser):
  total_wins = models.IntegerField(default=0)
  total_losses = models.IntegerField(default=0)
  friends = models.ManyToManyField("CustomUser", blank=True)
  blocked_users = models.ManyToManyField("CustomUser", blank=True, related_name="blocked_by")
  last_online = models.DateTimeField(blank=True, null=True)
  
  def __str__(self):
    return self.username
  
  def is_online(self):
    if self.last_online:
      return (timezone.now() - self.last_online) < timezone.timedelta(minutes=15)
    return False

  def get_online_info(self):
    if self.is_online():
      return _('Online')
    if self.last_online:
      return _('Last visit {}').format(naturaltime(self.last_online))
    return _('Unknown')

  
class FriendRequest(models.Model):
  from_user = models.ForeignKey(
    CustomUser, related_name='from_user', on_delete=models.CASCADE
  )
  to_user = models.ForeignKey(
    CustomUser, related_name='to_user', on_delete=models.CASCADE
  )
