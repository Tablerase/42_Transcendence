from game.models import Match, Player

from channels.db import database_sync_to_async
from django.db import transaction

class MatchInfo:
  def __init__(self, tournament_id, group_name, channel_layer, match_id):
    self.tournament_id = tournament_id
    self.group_name = group_name
    self.channel_layer = channel_layer
    self._scores = [0, 0]
    self._name = None
    self._player_names = []
    self.match_id = match_id 
    self.left_paddle = None
    self.right_paddle = None
    
  async def initialize(self):
    await self.set_match_info(self.match_id)
  
  @database_sync_to_async
  def set_match_info(self, match_id):
    match = Match.objects.get(id=match_id)
    self._name = str(match)
    self._player_names = [ player for player in match.players.all()]
    self.left_paddle = match.left_paddle
    self.right_paddle = match.right_paddle
    print(self.left_paddle)
    print(self.right_paddle)
    
  # Getters.

  def get_scores(self):
    if self._scores is None:
      self._scores = [0, 0]
    return self._scores

  def get_player_names(self):
    return self._player_names
  
  def get_name(self):
    return self._name
  
  # Setters.
  
  def set_message(self, message):
    self._name = message

  # Scores.

  def reset_scores(self):
    self._scores = [0, 0]
  
  async def increment_score(self, player, index):
    self._scores[index] += 1
    await self.increment_in_database(player)

  @database_sync_to_async
  def increment_in_database(self, user):
    with transaction.atomic():
      match = Match.objects.select_for_update().get(id=self.match_id)
      player = Player.objects.select_for_update().get(match=match, user=user)
      player.add_points(1)
      if player.points == 10:
        player.set_winner()
      
  @database_sync_to_async
  def get_player_score(self, user):
    match = Match.objects.get(id=self.match_id)
    player = Player.objects.get(match=match, user=user)
    return player.points

  def __str__(self) -> str:
    players = ', '.join(str(player) for player in self._player_names)
    return (
      f"Match Info:\n"
      f"Tournament ID: {self.tournament_id}\n"
      f"Group Name: {self.group_name}\n"
      f"Match Name: {self._name}\n"
      f"Players: {players}\n"
      f"Scores: {self._scores[0]} - {self._scores[1]}"
    )

    
