from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import gettext_lazy as _
from game.models import Match, Player, Tournament

class CustomUser(AbstractUser):
  total_wins = models.IntegerField(default=0)
  total_losses = models.IntegerField(default=0)
  friends = models.ManyToManyField("CustomUser", blank=True)
  blocked_users = models.ManyToManyField("CustomUser", blank=True, related_name="blocked_by")
  last_online = models.DateTimeField(blank=True, null=True)
  
  def __str__(self):
    return self.username
  
  def is_online(self):
    return self.last_online and (timezone.now() - self.last_online) < timezone.timedelta(minutes=5)

  def get_online_info(self):
    if self.is_online():
        return _('Online')
    if self.last_online:
        return _('Last visit {}').format(naturaltime(self.last_online))
    return _('Unknown')
  
  def get_match_set(self):
    match_set = Match.objects.filter(players=self).order_by('-played_at')[:5]
    matches = []
    for match in match_set:
      self_user = match.players.filter(id=self.id).first()
      other_user = match.players.exclude(id=self.id).first()
      self_player = Player.objects.get(match=match, user=self)
      other = Player.objects.get(match=match, user=other_user)

      match_info = {
        'tournament': match.tournament.name,
        'date': match.played_at if match.played_at else None,
        'self_points': self_player.points, 
        'self_username': self_player.user,
        'self_avatar': self_user.profile.image.url,
        'other_points': other.points, 
        'other_username': other.user,
        'other_avatar': other_user.profile.image.url,
      }
      matches.append(match_info)
    return matches
