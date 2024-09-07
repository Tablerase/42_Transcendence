import django
from django.db import models
from PIL import Image
from django.conf import settings

class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  image = models.ImageField(default='default.jpg', upload_to='profile_pics')
  
  def __str__(self):
    return f'{self.user.username} Profile'  
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    try:
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
        img.thumbnail(output_size, Image.ANTIALIAS)
        img.save(self.image.path)
    
    except IOError:
      print("Error in processing the image")
