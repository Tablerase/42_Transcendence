from game.models import Match, Player

from channels.db import database_sync_to_async

class MatchInfo:
  def __init__(self, tournament_id, group_name, channel_layer, match_id):
    self.tournament_id = tournament_id
    self.group_name = group_name
    self.channel_layer = channel_layer
    self._scores = [0, 0]
    self._name = None
    self._player_names = []
    self.match_id = match_id
    
  async def initialize(self):
    await self.set_match_info(self.match_id)
  
  @database_sync_to_async
  def set_match_info(self, match_id):
    match = Match.objects.get(id=match_id)
    self._name = str(match)
    self._player_names = [ player for player in match.players.all()]

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
  
  async def increment_score(self, player_index):
    self._scores[player_index] += 1
    await self.save_scores(player_index)

  @database_sync_to_async
  def save_scores(self, index):
    match = Match.objects.get(id=self.match_id)
    players = Player.objects.filter(match=match)
    player = players[index]
    player.add_points(1)
    if player.points == 10:
      player.set_winner()
      

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

    
