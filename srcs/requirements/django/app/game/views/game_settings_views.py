from game.models import Tournament

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from users.models.Customization_model import Customization
from users.forms import CustomizationForm

@login_required
def home(request):
  try:
    if request.method == "POST":
      mode = request.POST.get("mode")
      valid_modes = ['practice', 'join', 'host', 'settings', 'quit']
      if mode not in valid_modes:
        raise ValueError("Invalid mode") 
      elif mode == "practice":
        return redirect("practice")
      elif mode == "settings":
        return redirect("settings")
      elif mode == "quit":
        return redirect("logout")
      return redirect("init", mode=mode)
    else: 
      return render(request, "game/home.html", {})
  except ValueError as e:
    messages.error(request, str(e))

def join_tournament(request, tournament_code):
  try:
    tournament_code = int(tournament_code)
    tournament = Tournament.objects.get(id=tournament_code)
  except Exception as e:
    raise ValidationError("Tournament Does Not Exist or Access Code is Invalid.")
  if (request.user in tournament.players.all()):
    return tournament.id
  if (tournament.players.count() >= 4 or tournament.status != 'open'):
    raise ValidationError("Tournament is full.")
  tournament.add_player(request.user)
  tournament.save()
  return tournament.id

def host_tournament(request, name):
  tournament = Tournament.objects.create(name=name, host=request.user)
  tournament.full_clean()
  tournament.save()
  return tournament.id

@login_required
def init(request, mode="join"):
  options = [
    {"key": "join", "handle_request": join_tournament, "message": "event code"},
    {"key": "host", "handle_request": host_tournament, "message": "event name"}
  ]
  try :
    selected_option = next((opt for opt in options if opt["key"] == mode), None)
    if selected_option is None:
      raise ValueError("Invalid mode")
    if request.method == "POST":
      data = request.POST.get("data") 
      if data is None:
        raise ValueError("Invalid data")
      tournament_id = selected_option["handle_request"](request, data)
      return redirect("tournament", tournament_id=tournament_id)
    else:
      context = {
        "mode": selected_option["key"],
        "header": selected_option["message"]
      }
      return render(request, "game/init.html", context)
  except ValueError as e:
    error_message = str(e)
  except ValidationError as e:
    error_message = ' '.join(e.messages)
  request.session['modal_data'] = {
    'template': '_error_modal.html',
    'title': 'Error',
    'message': error_message
  }
  return redirect("init", mode=mode)

@login_required
def settings(request):
  customization, created = Customization.objects.get_or_create(user=request.user)
  
  ball_options = [
    {'value': 'asteroid', 'image': 'game/images/⚽️/asteroid.png', 'alt': 'asteroid'},
    {'value': 'earth', 'image': 'game/images/⚽️/earth.png', 'alt': 'earth'},
    {'value': 'black-hole', 'image': 'game/images/⚽️/black-hole.png', 'alt': 'black hole'},
    {'value': 'disco-ball', 'image': 'game/images/⚽️/disco-ball.png', 'alt': 'disco ball'},
    {'value': 'marie-antoinette-head', 'image': 'game/images/⚽️/marie-antoinette-head.png', 'alt': 'marie antoinette head'},
    {'value': 'wool', 'image': 'game/images/⚽️/wool.png', 'alt': 'A kitten\'s favorite'}
  ]

  paddle_options = [
    {'value': '#EB3678', 'color': '#EB3678'},
    {'value': '#C0C0C0', 'color': '#C0C0C0'},
    {'value': '#8A2BE2', 'color': '#8A2BE2'},
    {'value': '#1E90FF', 'color': '#1E90FF'},
    {'value': '#00FF7F', 'color': '#00FF7F'},
    {'value': '#FF4500', 'color': '#FF4500'}
  ]

  context = {
    'current_ball': customization.ball,
    'current_paddle_color': customization.paddle_color,
    'ball_options': ball_options,
    'paddle_options': paddle_options
  }

  return render(request, 'game/settings.html', context)

@csrf_exempt
@login_required
def save_customization(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    ball = data.get('ball')
    paddle_color = data.get('paddle_color')
    
    customization, created = Customization.objects.get_or_create(user=request.user)
    customization.ball = ball
    customization.paddle_color = paddle_color
    customization.save()
    
    ball_display_name = customization.get_ball_display_name()
    paddle_color_display_name = customization.get_paddle_color_display_name()

    request.session['modal_data'] = {
      'template': '_success_modal.html',
      'title': 'Changes Saved',
      'message': f'You selected to use <i>{paddle_color_display_name}</i> paddles, with a <i>{ball_display_name}</i> ball.'
    }

    return JsonResponse({'success': True})
  return JsonResponse({'success': False})

@login_required
def reset_customization_to_default(request):
  if request.method == 'POST':
    customization, created = Customization.objects.get_or_create(user=request.user)
    customization.ball = 'asteroid'
    customization.paddle_color = '#EB3678'
    customization.save()

    ball_display_name = customization.get_ball_display_name()
    paddle_color_display_name = customization.get_paddle_color_display_name()

    
    request.session['modal_data'] = {
      'template': '_success_modal.html',
      'title': 'Defaults Restored',
      'message': 'Your settings have been reset to default values: '
                  f'<i>{paddle_color_display_name}</i> paddles and a <i>{ball_display_name}</i> ball.'
      }

    return JsonResponse({'success': True})
  return JsonResponse({'success': False})
