# Library imports

# Django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Local app imports
import game.helpers.utils as utils
from game.models import Tournament


@login_required
def settings(request):
  return render(request, "game/settings.html", {})

@login_required
def practice(request):
  return render(request, "game/practice.html", {})

@login_required
@require_POST
def quit(request, tournament_id):
  try:
    tournament = Tournament.objects.get(id=tournament_id)
    if request.POST.get("quit_button") == "quit":
      if (tournament.host.id == request.user.id):
        tournament.remove_host()
      else:
        tournament.remove_player(request.user)
      return redirect("home")
    subtitle = "Attempting to re-enter the tournament may not be possible."
    return render(request, 'game/quit.html', {"tournament_id": tournament_id, "subtitle": subtitle})
  except Tournament.DoesNotExist:
    request.session['modal_data'] = {
      'template': '_error_modal.html',
      'title': 'Error',
      'message': 'Tournament does not exist'
    }
  return redirect("home")


@login_required
def tournament(request, tournament_id):
  try:
    user = request.user
    tournament = Tournament.objects.get(id=tournament_id)
    if (user not in tournament.players.all()):
      utils.join_tournament(request, tournament_id)
    #if request.method == "POST": # later on this will be a websocket event
    #  if user.id != tournament.host.id:
    #    raise ValueError("You can't start this tournament because you are not the host.")
    #  tournament.generate_matches()  
    context = {
      "tournament": tournament,
    }
    return render(request, "game/tournament.html", context)   
  except ValidationError as e:
    error_message = ' '.join(e.messages)
    request.session['modal_data'] = {
      'template': '_error_modal.html',
      'title': 'Action Denied. ⚠️',
      'message': error_message
    }
  except ValueError as e:
    request.session['modal_data'] = {
      'template': '_error_modal.html',
      'title': 'Action Denied. ⚠️',
      'message': str(e)
    }
  except Tournament.DoesNotExist:
    request.session['modal_data'] = {
      'template': '_error_modal.html',
      'title': 'Error',
      'message': 'Tournament does not exist'
    }
  return redirect("home")
    
@login_required
def init(request, mode="join"):
  options = [
    {"key": "join", "handle_request": utils.join_tournament, "message": "event code"},
    {"key": "host", "handle_request": utils.host_tournament, "message": "event name"}
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
def home(request):
  try:
    if request.method == "POST":
      mode = request.POST.get("mode")
      valid_modes = ['practice', 'join', 'host']
      if mode not in valid_modes:
        raise ValueError("Invalid mode") 
      if mode == "practice":
        return redirect("practice")
      return redirect("init", mode=mode)
    else: 
      return render(request, "game/home.html", {})
  except ValueError as e:
    messages.error(request, str(e))
  return redirect("home")

@csrf_exempt
def clear_modal_data(request):
  if request.method == 'POST':
    request.session.pop('modal_data', None)
    return JsonResponse({'status': 'success'})
  return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def clear_modal_data(request):
  if request.method == 'POST':
    request.session.pop('modal_data', None)
    return JsonResponse({'status': 'success'})
  return JsonResponse({'status': 'error'}, status=400)


@login_required
def index(request):
  return redirect("home")