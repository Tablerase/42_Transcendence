from game.models import Tournament
from users.models import CustomUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def join_tournament(request, tournament_code):
  try:
    tournament_code = int(tournament_code)
    tournament = Tournament.objects.get(id=tournament_code)
  except Exception as e:
    raise ValidationError("Tournament Does Not Exist or Access Code is Invalid.")
  if (tournament.players.count() >= 4 or tournament.locked):
    raise ValidationError("Tournament is full.")
  tournament.add_player(request.user)
  tournament.save()
  return tournament.id

def host_tournament(request, name):
  tournament = Tournament.objects.create(name=name, host=request.user)
  tournament.full_clean()
  tournament.save()
  return tournament.id


