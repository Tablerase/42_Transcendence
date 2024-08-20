from .models import FriendRequest

def get_user_context(current_user, user_list, requests=None):
  users_with_context = []

  for user in user_list:
    if user == current_user:
      continue

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
      'show_accept_button': show_accept_button,
      'user_friend': user_friend,
      'pending_request': pending_request,
      'request': request
    })

  return users_with_context