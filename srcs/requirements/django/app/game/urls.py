from django.urls import path

from .views.game_settings_views import home, settings, init, save_customization, reset_customization_to_default
from .views.modal_views import clear_modal_data
from .views.localplay_views import practice
from .views.tournament_views import tournament, leaderboard

urlpatterns = [
  path("", home, name="home"),
  path("home/", home, name="home"),
  path("practice/", practice, name="practice"),
  path("init/", init, name="init"),
  path("init/<str:mode>/", init, name="init"),
  path("tournament/<int:tournament_id>/", tournament, name="tournament"),
  path("settings/", settings, name="settings"),
  path('save_customization/', save_customization, name='save_customization'),
  path('reset_customization_to_default/', reset_customization_to_default, name='reset_customization_to_default'),
  path('clear_modal_data/', clear_modal_data, name='clear_modal_data'),
  path('leaderboard/', leaderboard, name='leaderboard'),
]