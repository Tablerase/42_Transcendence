import asyncio

from channels.db import database_sync_to_async

import game.helpers.game.utils.utils as utils
import game.helpers.game.utils.websocket_utils as ws_utils
from game.models import Match

async def handle_move(move, role, engine):
  if role not in  ['left_paddle', 'right_paddle']:
    return
  asyncio.create_task(engine.receive_message_from_consumer(move, role))

@database_sync_to_async
def start_next_match(tournament):
  match = tournament.get_next_match()
  if match is None:
    return None, None
  match.start()
  return str(match), match.id

async def get_match_context(match_id, user):
  match = await get_match_info(match_id)
  role = await assign_roles(match, user)
  context = {
    'message': 'start_tournament',
    'match': match['match'],
    'role': role
  }
  return context

@database_sync_to_async
def get_match_info(match_id):
  match = Match.objects.get(id=match_id)
  match_info = {
    'id': match_id,
    'match': str(match),
    'players': [ player.id for player in match.players.all()]
  }
  return match_info

@database_sync_to_async
def assign_roles(match, user):
  players = match['players']
  if user.id == players[0]:
    return 'left_paddle'
  elif user.id == players[1]:
    return 'right_paddle'
  else:
    return 'spectator'
  

  

