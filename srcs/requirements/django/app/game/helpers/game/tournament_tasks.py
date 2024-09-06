import asyncio
from channels.layers import get_channel_layer
from django.core.exceptions import ValidationError

import game.helpers.game.utils.utils as utils
import game.helpers.game.utils.websocket_utils as ws_utils
import game.helpers.game.pages.match as trn
from game.helpers.game.classes.GameClass import Game
from game.helpers.game.classes.MatchInfoClass import MatchInfo
from game.models import Tournament

class TournamentEngine:
  def __init__(self, tournament_id, group_name):
    self.tournament_id = tournament_id
    self.group_name = group_name
    self.channel_layer = get_channel_layer()

  async def run_tournament(self):
    tournament = await utils.get_tournament(self.tournament_id)
    await utils.lock_tournament(tournament)
    try:
      while True:
        tournament = await utils.get_tournament(self.tournament_id)
        match_name, match_id = await trn.start_next_match(tournament)
        if match_name is None:
          await self.complete_tournament()
          break
        await ws_utils.send_message_to_group(self, 'start_match', match_id=match_id)
        for i in range(5, -1, -1):
          await ws_utils.send_message_to_group(self, 'countdown_message', count=i)
          await asyncio.sleep(1)
        await self.start_game( match_id)
    except (Tournament.DoesNotExist, ValidationError) as error:
      error_message = error.messages[0] if error.messages else str(error)
      await ws_utils.send_message_to_group(
        self,
        'modal',
        message='modal',
        title='Action Denied. ⚠️',
        error_message=error_message
      )

  
  async def start_game(self, match_id):
    match_info = MatchInfo(self.tournament_id, self.group_name, self.channel_layer, match_id=match_id)
    await match_info.initialize()
    self.game = Game(match_info)
    await self.game.game_loop()  # Await the game loop


  async def receive_message_from_consumer(self, message, role):
    if not hasattr(self, 'game'):
      return
    if message in ['up', 'down']:
      direction = message
      paddle_name = role 
      await self.game.move_paddle(paddle_name, direction)

  async def complete_tournament(self):
    await utils.close_tournament(self.tournament_id)
    await ws_utils.send_message_to_group(self, 'get_results')