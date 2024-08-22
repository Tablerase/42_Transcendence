from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from users.utils import get_user_context
from django.urls import reverse
from users.models import FriendRequest
from django.http import JsonResponse
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
    searched = request.POST.get('searched', '').strip()
    if searched:
      users = CustomUser.objects.filter(
        Q(username__icontains=searched) | Q(email__icontains=searched)
      )
    else:
      users = CustomUser.objects.none()
    context = {
      'searched': searched,
      'users': users,
      'active_button': 'all_users'
    }
    return render(request, 'users/listing/users_search.html', context)
  else:
    return render(request, 'users/listing/users_search.html', {})

def update_user_score(user_id, won):
  user = CustomUser.objects.get(pk=user_id)
  if won:
      user.total_wins += 1
  else:
      user.total_losses += 1
  user.save()
  
@login_required
def send_friend_request(request, userID):
  from_user = request.user
  to_user = CustomUser.objects.get(id=userID)
  friend_request, created = FriendRequest.objects.get_or_create(
    from_user=from_user, to_user=to_user
  )
  
  if created:
    return JsonResponse({
      'status': 'pending',
      'icon': 'bi bi-hourglass-split text-warning'
    })
  return JsonResponse({'status': 'already_sent'})

@login_required
def accept_friend_request(request, requestID):
  friend_request = FriendRequest.objects.get(id=requestID)
  
  if friend_request.to_user == request.user:
    friend_request.to_user.friends.add(friend_request.from_user)
    friend_request.from_user.friends.add(friend_request.to_user)
    friend_request.delete()

    return JsonResponse({
      'status': 'friend',
      'icon': 'bi bi-person-x-fill text-danger'
    })
  else:
    return JsonResponse({'status': 'error'})
  
@login_required
def remove_friend(request, userID):
  current_user = request.user
  friend_to_remove = get_object_or_404(CustomUser, id=userID)
  current_user.friends.remove(friend_to_remove)
  friend_to_remove.friends.remove(current_user)
  
  return JsonResponse({
    'status': 'not_friend',
    'icon': 'bi bi-person-plus'
  })
  
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

@login_required
def cancel_friend_request(request, user_id):
  friend_request = get_object_or_404(FriendRequest, from_user=request.user, to_user_id=user_id)
  friend_request.delete()

  return redirect(request.META.get('HTTP_REFERER', 'view_friends'))