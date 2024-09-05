from itertools import combinations
from random import choice

import django
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models

class Tournament(models.Model):
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
  choices = [ 
      ('open', 'open'),
      ('locked', 'locked'),
      ('closed', 'closed')
  ]
  status = models.CharField(
    max_length=10,
    choices=choices,
    default='open'
  )
  
  created_at = models.DateTimeField(auto_now_add=True)

  def get_leaderboard(self):
    if self.status != 'closed':
      raise ValidationError("Tournament is not closed")
    leaderboard = []
    for player in self.players.all():
      total_points = 0
      matches = Match.objects.filter(tournament=self)
      for match in matches:
        match_player = Player.objects.filter(match=match, user=player).first()
        if match_player:
          total_points += match_player.points
      leaderboard.append({
        'username': player.username,
        'points': total_points,
        'image_url': player.profile.image.url
      })
    leaderboard.sort(key=lambda x: x['points'], reverse=True)
    if leaderboard:
      winner_username = leaderboard[0]['username']
      self.winner = self.players.get(username=winner_username)
      self.save()
    return leaderboard


  def get_next_match(self):
    return self.match_set.filter(status='pending').first()
  
  def get_match_in_progress(self):
    matches_in_progress = self.match_set.filter(status='in_progress')
    if matches_in_progress.count() > 1:
      raise ValidationError("There is more than one match in progress.")
    if not matches_in_progress.exists():
      raise ValidationError("There is no match in progress.")
    return matches_in_progress.first()
  
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
    self.status = 'locked'
    self.save()
  
  def add_player(self, player):
    if self.players.count() == 4 or self.status != 'open':
      raise ValidationError("Tournament is full")
    self.players.add(player)
  
  def remove_host(self):
    if not self.pk:
      self.save()
    self.players.remove(self.host)
    available_players = self.players.exclude(id=self.host.id)
    if available_players.exists():
      self.host = choice(available_players)
      self.save()
    else:
      self.delete()

  def remove_player(self, player_id):
    if self.host.id == player_id:
      self.remove_host()
    else:
      self.players.remove(player_id)
      self.save()
      
  def __str__(self):
    return self.name
  
  def save(self, *args, **kwargs):
    self.full_clean()
    super().save(*args, **kwargs)
    if not self.players.filter(id=self.host.id).exists():
      self.players.add(self.host)


class Match(models.Model):
  tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  players = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    through='Player'
  )
  status = models.CharField(
    max_length=11,
    choices=[
      ('pending', 'pending'),
      ('in_progress', 'in_progress'),
      ('finished', 'finished')],
    default='pending' 
  )
  played_at = models.DateTimeField(null=True, blank=True)
  
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

  def start(self):
    self.status = 'in_progress'
    self.save()

  def finish(self):
    self.played_at = timezone.now()
    self.status = 'finished'
    players = Player.objects.filter(match=self)
    for player in players:
      player.update_user()
    self.save()


class Player(models.Model):
  match = models.ForeignKey(Match, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  points = models.IntegerField(default=0)
  is_winner = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.user} in {self.match}"
  
  class Meta:
    unique_together = [('match', 'user')]

  def add_points(self, points):
    self.points += points
    self.save()
  
  def update_user(self):
    if self.is_winner:
      self.user.total_wins += 1
    else:
      self.user.total_losses += 1
    self.user.save()
  
  def set_winner(self):
    self.is_winner = True
    self.save()
    self.match.finish()
    self.match.save()

