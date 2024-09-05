import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ValidationError

import game.helpers.game.pages.lobby as lobby
import game.helpers.game.pages.match as trn
import game.helpers.game.pages.results as results
import game.helpers.game.tournament_tasks as tasks
import game.helpers.game.utils.websocket_utils as ws_utils
import game.helpers.game.utils.utils as utils
from game.models import Tournament, Match

class TournamentConsumer(AsyncWebsocketConsumer):

  engines = {}

  async def connect(self):
    print("Trying to connect.")
    ws_utils.authenticate_and_initialize(self)
    try:
      print("We are here too.")
      tournament = await utils.get_tournament(self.tournament_id)
      await lobby.register_player_in_tournament(tournament, self.user)
      await ws_utils.add_channel_to_group_and_accept(self)
      if await utils.get_tournament_status(tournament) == 'open':
        print("Here as well.")
        await ws_utils.send_message_to_group(self, 'lobby_update')
      elif await utils.get_tournament_status(tournament) == 'locked':
        await ws_utils.send_message_to_group(self, 'start_match')
      else:
        await ws_utils.send_message_to_group(self, 'get_results')
    except (Tournament.DoesNotExist, ValidationError, Match.DoesNotExist) as e:
      print("Error here." + str(e))
      await self.handle_exception('Error', e)

  async def disconnect(self, close_code):
    print(f"Disconnecting {close_code}")
    await ws_utils.discard_channel_from_group(self)

  async def receive(self, text_data): 
    data = json.loads(text_data) 
    await self.parseData(data)

  async def parseData(self, data): 
    try:
      if data['message'] == 'leave_tournament':
        await lobby.unregister_player_from_tournament(self)
      elif data['message'] == 'start_tournament':
        await self.start_tournament_engine()
      elif data['message'] in ['up', 'down']:
        await self.get_tournament_engine()
        if self.role in ['left_paddle', 'right_paddle']:
          asyncio.create_task(self.engine.receive_message_from_consumer(data['message'], self.role))
      else:
        raise ValidationError("Ah ah ah, you didn't say the magic word!")
    except ValidationError as e:
      await self.display_modal('Action Denied. ⚠️', e)

  async def start_tournament_engine(self):
    if self.tournament_id not in TournamentConsumer.engines:
      # Check there are at least 2 players
      tournament = await utils.get_tournament(self.tournament_id)
      await utils.tournament_has_enough_players(tournament)
      engine = tasks.TournamentEngine(self.tournament_id, self.group_name)
      TournamentConsumer.engines[self.tournament_id] = engine
      asyncio.create_task(engine.run_tournament())

  async def get_tournament_engine(self):
    if not hasattr(self, 'engine') or not self.engine:
      if self.tournament_id in TournamentConsumer.engines:
        self.engine = TournamentConsumer.engines[self.tournament_id]
    return self.engine
  
  async def lobby_update(self, event):
    try:
      tournament = await utils.get_tournament(self.tournament_id)
      context = await lobby.get_lobby_context(tournament)
      await self.send(text_data=json.dumps(context))
    except Tournament.DoesNotExist as e:
      await self.handle_exception('Error', e)
  
  async def start_match(self, event):
    try:
      match_id = event.get('match_id', None)
      if (match_id is None):
        match_id = await utils.get_match_in_progress(self.tournament_id)
      match_context = await trn.get_match_context(match_id, self.user)
      self.role = match_context['role']
      await self.send(text_data=json.dumps(match_context))
    except (Tournament.DoesNotExist, Match.DoesNotExist, ValidationError) as e:
      await self.handle_exception('Error', e)

  async def game_state(self, event):
    game_state = event.get('game_state', None)
    await self.send(text_data=json.dumps(game_state))
  
  async def get_results(self, event):
    results_context = await results.get_results_context(self.tournament_id)
    await self.send(text_data=json.dumps(results_context))


  async def countdown_message(self, event):
    countdown = event.get('count', 0)
    context = {
      'message': 'countdown',
      'count': countdown
    }
    await self.send(text_data=json.dumps(context))

  async def modal(self, event):
    modal_context = {
      'message': 'modal',
    }
    await self.send(text_data=json.dumps(modal_context))

  async def handle_exception(self, title, e):
    error_message = e.messages[0] if e.messages else str(e)
    await utils.store_error_in_session(self, title, error_message)
    self.close(1000)

  async def display_modal(self, title, error):
    error_message = error.messages[0] if error.messages else str(error)
    await utils.store_error_in_session(self, title, error_message)
    await ws_utils.send_message_to_group(self, 'modal')