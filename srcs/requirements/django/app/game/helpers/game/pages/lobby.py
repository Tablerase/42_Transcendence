import game.helpers.game.utils.utils as utils
import game.helpers.game.utils.websocket_utils as ws_utils

from django.core.exceptions import ValidationError


async def register_player_in_tournament(tournament, player):
  if not await utils.is_user_in_tournament(player, tournament):
    if not await utils.can_anyone_join_tournament(tournament):
      raise ValidationError("Tournament is closed to newcomers.")
    await utils.add_player_to_tournament(tournament, player)


async def get_lobby_context(tournament):
  players = await utils.get_tournament_players(tournament.players.all())
  host = await utils.get_tournament_host(tournament)
  context =  {
    'message': 'lobby_update',
    'players': players,
    'host_id': host.id
  }
  return context

async def unregister_player_from_tournament(consumer):
  tournament = await utils.get_tournament(consumer.tournament_id)
  await utils.remove_player_from_tournament(tournament, consumer.user.id)
  if await utils.tournament_exists(tournament.id):
    await ws_utils.send_message_to_group(consumer, 'lobby_update')
  await consumer.disconnect(1000)


  
