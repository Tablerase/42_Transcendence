from .models import FriendRequest
from collections import namedtuple
from django.contrib.auth import get_user_model

def get_user_context(current_user, user_list, requests=None):
  users_with_context = []

  for user in user_list:
    if user == current_user:
      continue
    
    user_blocked = user in current_user.blocked_users.all()

    if user in current_user.friends.all():
      user_friend = True
      show_accept_button = False
      pending_request = False
      request = None
    elif FriendRequest.objects.filter(from_user=current_user, to_user=user).exists():
      user_friend = False
      show_accept_button = False
      pending_request = True
      request = None
    else:
      friend_request = FriendRequest.objects.filter(from_user=user, to_user=current_user).first()
      user_friend = False
      show_accept_button = friend_request is not None
      pending_request = False
      request = friend_request

    users_with_context.append({
      'user': user,
      'user_friend': user_friend,
      'user_blocked': user_blocked,
      'show_accept_button': show_accept_button,
      'request': request,
      'pending_request': pending_request,
    })

  return users_with_context

CustomUser = get_user_model()
Match = namedtuple('Match', ['id', 'user1', 'user2', 'user1_score', 'user2_score', 'date', 'tournament'])

def generate_dummy_matches(user1):
  user2, created = CustomUser.objects.get_or_create(username='opponent', defaults={'password': 'password123'})
  
  dummy_matches = [
    Match(id=1, user1=user1, user2=user2, user1_score=3, user2_score=10, date="2024-08-26 20:00", tournament="Summer Tournament"),
    Match(id=2, user1=user1, user2=user2, user1_score=10, user2_score=8, date="2024-08-25 18:00", tournament="Spring Championship"),
    Match(id=3, user1=user1, user2=user2, user1_score=10, user2_score=3, date="2024-08-24 16:00", tournament="Autumn Open"),
    Match(id=4, user1=user1, user2=user2, user1_score=8, user2_score=10, date="2024-08-27 21:42", tournament="Clash"),
  ]
  
  return dummy_matches
  