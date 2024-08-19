# Consumers for the websocket_game application.

import json
import uuid

from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class GameConsumer(WebsocketConsumer):
    game_group_name = "game_group"
    players = {}

    # At initial connection
    def connect(self):
        self.player_id = str(uuid.uuid4())
        self.accept()
    
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name, self.channel_name
        )
        
        # Send the player ID to the client
        self.send(
            text_data=json.dumps({
                "type":"playerId",
                "playerId":self.player_id
            })
        )
    
    # At disconnected
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )
    
    # When a message is received
    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                text_data_json = json.loads(text_data)
                # Process the JSON data
            except json.JSONDecodeError:
                # Handle the error (e.g., log it, send an error message back to the client, etc.)
                self.send(text_data=json.dumps({'error': 'Invalid JSON received'}))
        else:
            # Handle the case where text_data is None or empty
            self.send(text_data=json.dumps({'error': 'No data received'}))