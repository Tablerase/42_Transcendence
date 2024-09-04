from channels.db import database_sync_to_async
from django.core.exceptions import ValidationError

from game.models import Tournament, Match

@database_sync_to_async
def get_tournament(tournament_id):
  return Tournament.objects.get(id=tournament_id)


@database_sync_to_async
def get_match_in_progress(tournament_id):
  tournament = Tournament.objects.get(id=tournament_id)
  match = tournament.get_match_in_progress()
  return match.id


@database_sync_to_async
def is_user_in_tournament(user, tournament):
  return user in tournament.players.all()

@database_sync_to_async
def can_anyone_join_tournament(tournament):
  return tournament.players.count() < 4 and tournament.status == 'open'

@database_sync_to_async
def add_player_to_tournament(tournament, player):
  tournament.add_player(player)

@database_sync_to_async
def tournament_exists(tournament_id):
  return Tournament.objects.filter(id=tournament_id).exists()

@database_sync_to_async
def get_next_match(tournament):
  return tournament.get_next_match()

@database_sync_to_async
def remove_player_from_tournament(tournament, player_id):
  tournament.remove_player(player_id)


@database_sync_to_async
def get_tournament_players(players): 
  return [
    {
      'id': player.id,
      'username': player.username,
      'image_url': player.profile.image.url,
      'wins': player.total_wins,
      'losses': player.total_losses,
    }
    for player in players.all()
  ]

@database_sync_to_async
def get_tournament_host(tournament):
  return tournament.host

@database_sync_to_async
def get_tournament_status(tournament):
  return tournament.status

@database_sync_to_async
def close_tournament(tournament_id):
  tournament = Tournament.objects.get(id=tournament_id)
  tournament.status = 'closed'
  tournament.save()

@database_sync_to_async
def tournament_has_enough_players(tournament):
  if tournament.players.count() < 2:
    raise ValidationError("You need at least 2 players to start the tournament.")

@database_sync_to_async
def lock_tournament(tournament):
  tournament.generate_matches()

# This function works in an http style... it will be fixed later.
@database_sync_to_async
def store_error_in_session(consumer, title, message):
  session = consumer.scope["session"]
  session['modal_data'] = {
    'template': '_error_modal.html',
    'title': title,
    'message': message
  }
  session.save()