# Routing for the websocket connection
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/test/(?P<room_name>\w+)/$', consumers.GameConsumer.as_asgi()),
    # re_path(r'ws/game/$', consumers.GameConsumer.as_asgi()),
]