from django.urls import re_path
from .consumers import TournamentConsumer

websocket_urlpatterns = [
    re_path(r'ws/tournament/(?P<tournament_id>\w+)/$', TournamentConsumer.as_asgi()),
]
