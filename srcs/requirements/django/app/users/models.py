from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.conf import settings
from django.templatetags.static import static


class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  image = models.ImageField(default='default.jpg', upload_to='profile_pics')
  image_url = models.URLField(blank=True, null=True)
  
  def __str__(self):
    return f'{self.user.username} Profile'
  
  def save(self, *args, **kwargs):
    if self.image and not self.image_url:
      super().save(*args, **kwargs)
      
      img = Image.open(self.image.path)
      
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
        
      img.save(self.image.path)
    else:
      super().save(*args, **kwargs)
      
  @property
  def profile_image_url(self):
    if self.image_url:
      return self.image_url
    elif self.image and self.image.url:
      return self.image.url if self.image else None
    else:
      return static('users/images/default-avatar.png')
      
    
class CustomUser(AbstractUser):
  total_wins = models.IntegerField(default=0)
  total_losses = models.IntegerField(default=0)
  friends = models.ManyToManyField("CustomUser", blank=True)
  blocked_users = models.ManyToManyField("CustomUser", blank=True, related_name="blocked_by")

  def __str__(self):
    return self.username
  
class FriendRequest(models.Model):
  from_user = models.ForeignKey(
    CustomUser, related_name='from_user', on_delete=models.CASCADE
  )
  to_user = models.ForeignKey(
    CustomUser, related_name='to_user', on_delete=models.CASCADE
  )
