from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models.FriendRequest_model import FriendRequest
from django.conf import settings
from users.models.User_model import CustomUser

@login_required
def send_friend_request(request, userID):
  from_user = request.user
  to_user = get_object_or_404(CustomUser, id=userID)
  friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
  
  if created:
    request.session['modal_data'] = {
      'template': '_success_modal.html',
      'title': 'Friend Request Sent',
      'message': f'L\'ets hope <b><u>{to_user.username}</b></u> wants to be your friend (ᵕ—ᴗ—).'
    }
  else:
    request.session['modal_data'] = {
      'template': '_success_modal.html',
      'title': 'Friend Request Already Sent',
      'message': f'You have already sent a friend request to <b><u>{to_user.username}</b></u> 🤌⏳🙇🏻.'
    }

  return redirect(request.META.get('HTTP_REFERER', 'users'))

@login_required
def cancel_friend_request(request, requestID=None, userID=None):
  if requestID:
    friend_request = get_object_or_404(FriendRequest, id=requestID)
  elif userID:
    friend_request = get_object_or_404(FriendRequest, from_user=request.user, to_user_id=userID)
  else:
    return redirect('view_friend_requests')

  friend_request.delete()

  request.session['modal_data'] = {
    'template': '_success_modal.html',
    'title': 'Friend Request Canceled',
    'message': 'Who\'d wanna be friends with that weirdo anyway right? 🙅‍♂️🗑️'
  }

  return redirect(request.META.get('HTTP_REFERER', 'view_friend_requests'))

@login_required
def accept_friend_request(request, requestID):
  friend_request = get_object_or_404(FriendRequest, id=requestID)
  
  if friend_request.to_user == request.user:
    friend_request.to_user.friends.add(friend_request.from_user)
    friend_request.from_user.friends.add(friend_request.to_user)
    friend_request.delete()

    request.session['modal_data'] = {
      'template': '_success_modal.html',
      'title': 'Friend Request Accepted',
      'message': f'You are now friends with <b><u>{friend_request.from_user.username}</b></u> ٩( ᐛ )( ᐖ )۶.'
    }

  return redirect(request.META.get('HTTP_REFERER', 'view_friend_requests'))

@login_required
def reject_friend_request(request, requestID):
  friend_request = get_object_or_404(FriendRequest, id=requestID)

  if friend_request.to_user == request.user:
    friend_request.delete()

    request.session['modal_data'] = {
      'template': '_success_modal.html',
      'title': 'Friend Request Rejected',
      'message': 'No thank you  •ᴗ• .'
    }

  return redirect(request.META.get('HTTP_REFERER', 'view_friend_requests'))
  
@login_required
def remove_friend(request, userID):
  current_user = request.user
  friend_to_remove = get_object_or_404(CustomUser, id=userID)
  current_user.friends.remove(friend_to_remove)
  friend_to_remove.friends.remove(current_user)

  request.session['modal_data'] = {
    'template': '_success_modal.html',
    'title': 'Friend Removed',
    'message': f'You\'ve removed <b><u>{friend_to_remove.username}</b></u> from your friends list ☠️🔪.'
  }

  return redirect(request.META.get('HTTP_REFERER', 'view_friends'))
