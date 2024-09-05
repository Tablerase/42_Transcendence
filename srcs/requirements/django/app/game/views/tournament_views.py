import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from game.models import Tournament
from users.models.Customization_model import Customization

@login_required
def tournament(request, tournament_id):
  try:
    tournament = Tournament.objects.get(id=tournament_id)
    customization, created = Customization.objects.get_or_create(user=request.user)
    ball_images = {
      'asteroid': 'game/images/⚽️/asteroid.png',
      'earth': 'game/images/⚽️/earth.png',
      'black-hole': 'game/images/⚽️/black-hole.png',
      'disco-ball': 'game/images/⚽️/disco-ball.png',
      'marie-antoinette-head': 'game/images/⚽️/marie-antoinette-head.png',
    }
    
    tournament_data = {
      'id': tournament.id,
      'name': tournament.name,
      'status': tournament.status,
      'host_name': tournament.host.username,
      'host_id': tournament.host.id,
      'user_id': request.user.id,
    }
    tournament_json = json.dumps(tournament_data)
    
    context = {
      "tournament": tournament,
      "tournament_json" : tournament_json,
      "user_customization": {
        "ball": customization.ball,
        "ball_display_name": customization.get_ball_display_name(),
        "ball_image": ball_images.get(customization.ball, ''),
        "paddle_color": customization.paddle_color,
        "paddle_color_display_name": customization.get_paddle_color_display_name(),
      }
    }
    return render(request, "game/tournament.html", context)

  except Tournament.DoesNotExist:
    request.session['modal_data'] = {
      'template': '_error_modal.html',
      'title': 'Error',
      'message': 'Tournament does not exist'
    }
    return redirect("home")
  
def leaderboard(request):
  return render(request, "game/leaderboard.html", {})  
  