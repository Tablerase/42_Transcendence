from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.conf import settings
from django.templatetags.static import static

class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  image = models.ImageField(default='default.jpg', upload_to='profile_pics')

  def __str__(self):
    return f'{self.user.username} Profile'

  def save(self, *args, **kwargs):
    # Save the instance first to ensure the image is available on the file system
    super().save(*args, **kwargs)

    # Open the image file
    if self.image:
      img_path = self.image.path  # Get the file path of the saved image
      img = Image.open(img_path)

      # Crop the image to a square if it is not square
      if img.height != img.width:
        min_dimension = min(img.height, img.width)
        left = (img.width - min_dimension) / 2
        top = (img.height - min_dimension) / 2
        right = (img.width + min_dimension) / 2
        bottom = (img.height + min_dimension) / 2
        img = img.crop((left, top, right, bottom))

      # Resize the image if it's larger than 300x300 pixels
      if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)

      # Save the modified image back to the same path
      img.save(img_path)

    
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
