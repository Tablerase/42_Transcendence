# Routing for the websocket connection
from django.urls import re_path
from . import consumers as game_consumers
from test import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<room_name>\w+)/$', game_consumers.GameConsumer.as_asgi()),
    # re_path(r'ws/game/$', consumers.GameConsumer.as_asgi()),
]