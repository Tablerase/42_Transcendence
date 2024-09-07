import django
from django.db import models
from django.conf import settings

class Customization(models.Model):
  BALL_CHOICES = [
    ('asteroid', 'Asteroid'),
    ('earth', 'Earth'),
    ('black-hole', 'Black Hole'),
    ('disco-ball', 'Disco Ball'),
    ('marie-antoinette-head', 'Marie Antoinette Head'),
    ('wool', 'Kitten\'s favorite')
  ]

  PADDLE_COLORS = [
    ('#EB3678', 'Cosmic Rose'),
    ('#C0C0C0', 'Starlight Silver'),
    ('#8A2BE2', 'Nebula Purple'),
    ('#1E90FF', 'Galactic Blue'),
    ('#00FF7F', 'Alien Green'),
    ('#FF4500', 'Solar Flare Orange'),
  ]

  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customization')
  ball = models.CharField(max_length=50, choices=BALL_CHOICES, default='asteroid')
  paddle_color = models.CharField(max_length=7, choices=PADDLE_COLORS, default='#EB3678')

  def __str__(self):
    return f"Customization for {self.user.username}"
  
  def get_ball_display_name(self):
    return dict(self.BALL_CHOICES).get(self.ball, 'Unknown')

  def get_paddle_color_display_name(self):
    return dict(self.PADDLE_COLORS).get(self.paddle_color, 'Unknown')
  