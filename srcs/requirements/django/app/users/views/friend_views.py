from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from users.utils import get_user_context
from users.models import FriendRequest
from django.db.models import Q

CustomUser = get_user_model()

@login_required
def users_list(request):
  current_user = request.user
  users = CustomUser.objects.exclude(id=current_user.id)
  
  users_with_context = get_user_context(current_user, users)

  context = {
    'users_with_context': users_with_context,
    'active_button': 'all_users'
  }
  return render(request, 'users/listing/users_list.html', context)
  
@login_required
def users_search(request):
  if request.method == "POST":
    current_user = request.user
    searched = request.POST.get('searched', '').strip()
    if searched:
      users = CustomUser.objects.filter(
        Q(username__icontains=searched) | Q(email__icontains=searched)
        & ~Q(id=request.user.id)
      )
    else:
      users = CustomUser.objects.none()
    users_with_context = get_user_context(current_user, users)
    context = {
      'searched': searched,
      'users_with_context': users_with_context,
      'active_button': 'all_users'
    }
    return render(request, 'users/listing/users_search.html', context)
  else:
    return render(request, 'users/listing/users_search.html', {})

@login_required
def view_friend_requests(request):
  current_user = request.user
  friend_requests = FriendRequest.objects.filter(to_user=current_user)
  
  requests_dict = {fr.from_user.id: fr for fr in friend_requests}
  users = [fr.from_user for fr in friend_requests]
  users_with_context = get_user_context(current_user, users, requests=requests_dict)

  context = {
    'users_with_context': users_with_context,
    'active_button': 'friend_requests'
  }
  return render(request, 'users/listing/friend_requests.html', context)

@login_required
def view_friends(request):
  friends = request.user.friends.all()
  
  friends_with_context = get_user_context(request.user, friends)

  context = {
    'users_with_context': friends_with_context,
    'active_button': 'friends'
  }
  return render(request, 'users/listing/friend_list.html', context)
