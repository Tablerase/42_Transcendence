from itertools import combinations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models

class Tournament(models.Model):
  date = models.DateTimeField(auto_now_add=True)
  name = models.CharField(
    max_length=20,
    validators=[
      MaxLengthValidator(20),
      RegexValidator(
        regex=r'^[A-Za-z][A-Za-z0-9_]*$',
        message="Name must start with a letter and contain only letters, numbers, or underscores."
      )
    ]
  )
  players = models.ManyToManyField(
    settings.AUTH_USER_MODEL, 
    related_name='players'
  )
  winner = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='winner'
  )
  host = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='hosted_tournaments'
  )
  locked = models.BooleanField(default=False)
  
  def generate_matches(self):
    if self.players.count() < 2:
      raise ValidationError("You need at least 2 players to start the tournament.")
    player_list = list(self.players.all())
    match_combinations = combinations(player_list, 2)
    for player1, player2 in match_combinations:
      if Match.objects.filter(players=player1).filter(players=player2).filter(tournament=self).exists():
        continue
      match = Match.objects.create(tournament=self)
      match.add_players(player1, player2)
  
  def add_player(self, player):
    if self.players.count() == 4:
      raise ValidationError("Tournament is full")
    self.players.add(player)
  
  def remove_player(self, player):
    self.players.remove(player)
    if self.players.count() == 0:
      self.delete()
  
  def __str__(self):
    return self.name
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if not self.players.filter(id=self.host.id).exists():
      self.players.add(self.host)


class Match(models.Model):
  tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  players = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    through='Player'
  )
  
  def __str__(self):
    players = self.players.all()
    if players.count() == 2:
      player1, player2 = players
      return f"{player1} vs {player2}"
    else:
      return f"{players.count()} players"
  
  def clean(self):
      super().clean()
      if self.players.count() != 2:
          raise ValidationError("A match must have exactly 2 players")
      
  def add_players(self, player1, player2):
    if self.players.exists():
      raise ValidationError("Players have already been added to this match")
    Player.objects.create(match=self, user=player1)
    Player.objects.create(match=self, user=player2)


class Player(models.Model):
  match = models.ForeignKey(Match, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  points = models.IntegerField(default=0)
  is_winner = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.user} in {self.match}"
  
  class Meta:
    unique_together = [('match', 'user')]

# Create your models here.
class WsGame(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    players_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
