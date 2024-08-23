# Consumers for the websocket_game application.

import json
import uuid

from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# class GameConsumer(WebsocketConsumer):
#     game_group_name = "game_group"
#     players_positions = {}

#     def connect(self):
#         self.player_id = str(uuid.uuid4())
#         self.accept()

#         async_to_sync(self.channel_layer.group_add)(
#             self.game_group_name, self.channel_name
#         )

#         # Initialize player position
#         self.players_positions[self.player_id] = {'x': 0, 'y': 0}

#         # Send the player ID to the client
#         self.send(
#             text_data=json.dumps({
#                 "type": "playerId",
#                 "playerId": self.player_id
#             })
#         )

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.game_group_name, self.channel_name
#         )

#         # Remove player position
#         if self.player_id in self.players_positions:
#             del self.players_positions[self.player_id]

#     def receive(self, text_data=None, bytes_data=None):
#         if text_data:
#             try:
#                 text_data_json = json.loads(text_data)
#                 message_type = text_data_json.get('type')

#                 if message_type == 'updatePosition':
#                     # Update player position
#                     self.players_positions[self.player_id] = {
#                         'x': text_data_json['x'],
#                         'y': text_data_json['y']
#                     }

#                     # Broadcast updated positions to all clients
#                     async_to_sync(self.channel_layer.group_send)(
#                         self.game_group_name,
#                         {
#                             'type': 'broadcastPositions',
#                             'positions': self.players_positions
#                         }
#                     )
#                 else:
#                     # Handle other message types
#                     pass
#             except json.JSONDecodeError:
#                 self.send(text_data=json.dumps({'error': 'Invalid JSON received'}))
#         else:
#             self.send(text_data=json.dumps({'error': 'No data received'}))

#     def broadcastPositions(self, event):
#         positions = event['positions']
#         self.send(text_data=json.dumps({
#             'type': 'positions',
#             'positions': positions
#         }))