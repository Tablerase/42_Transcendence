from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from users.models.Customization_model import Customization

@login_required
def practice(request):
  customization = Customization.objects.filter(user=request.user).first()

  ball_image = customization.ball if customization else 'asteroid'
  paddle_color = customization.paddle_color if customization else '#C0C0C0'

  context = {
    'ball_image': ball_image,
    'paddle_color': paddle_color,
  }
  return render(request, "game/practice.html", context)