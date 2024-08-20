# Library imports

# Django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Local app imports
import game.helpers.utils as utils
from game.models import Match, Player, Tournament
#from users.models import CustomUser

@login_required
def pong(request):
  return render(request, "game/pong.html", {})

@login_required
def start(request, id):
  try:
    tournament = Tournament.objects.get(id=id)
    if request.user.id != tournament.host.id:
      raise ValueError("You are not the host of this tournament.")
    tournament.generate_matches()
    tournament.locked = True
    tournament.save()
    return redirect("pong")
  except ValueError as e:
    messages.error(request, str(e))
  except Tournament.DoesNotExist:
    messages.error(request, "Tournament does not exist")
  except ValidationError as e:
    error_message = ' '.join(e.messages)
    messages.error(request, error_message)
  return redirect("lobby", id=id)

@login_required
def quit(request, id):
  try:
    tournament = Tournament.objects.get(id=id)
    if request.method == "POST":
      if (tournament.host.id == request.user.id):
        tournament.players.clear()
        tournament.delete() # TODO: Make sure deletion takes every player out of the lobby.
      else:
        tournament.remove_player(request.user)
        tournament.save()
      return redirect("home")
    if request.user.id == tournament.host.id:
      subtitle = "Leaving the tournament will cancel the game for all players." 
    else:
      subtitle = "You will be removed from the tournament"
    return render(request, 'game/quit.html', {"id": id, "subtitle": subtitle})
  except Tournament.DoesNotExist :
    messages.error(request, "Tournament does not exist")
  return redirect("home")

@login_required
def lobby(request, id):
  try:
    tournament = Tournament.objects.get(id=id)
    if (request.user not in tournament.players.all()):
      raise ValueError("You are not in this tournament")
    mode = "host" if tournament.host.id == request.user.id else "join"
    context = {
      "tournament": tournament,
      "mode": mode }
    return render(request, "game/lobby.html", context)   
  except ValueError as e:
    messages.error(request, str(e))
  except Tournament.DoesNotExist:
    messages.error(request, "Tournament does not exist")
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
      id = selected_option["handle_request"](request, data)
      return redirect("lobby", id=id)
    else:
      context = {
        "mode": selected_option["key"],
        "header": selected_option["message"]
      }
      return render(request, "game/init.html", context)
  except ValueError as e:
    error_message = e.message
  except ValidationError as e:
    error_message = ' '.join(e.messages)
  messages.error(request, error_message)
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
        return redirect("pong")
      return redirect("init", mode=mode)
    else: 
      return render(request, "game/home.html", {})
  except ValueError as e:
    messages.error(request, str(e))
  return redirect("home")
