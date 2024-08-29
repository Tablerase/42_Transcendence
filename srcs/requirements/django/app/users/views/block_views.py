from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from users.models import CustomUser

@login_required
def block_user(request, userID):
  current_user = request.user
  user_to_block = get_object_or_404(CustomUser, id=userID)

  if user_to_block != current_user:
    current_user.blocked_users.add(user_to_block)
    current_user.friends.remove(user_to_block)
    
    request.session['modal_data'] = {
      'template': '_success_modal.html',
      'title': 'User Blocked',
      'message': f'You have blocked <b><u>{user_to_block.username}</b></u> 🚫🛡️.</br>You will no longer see messages from this user.'
    }

  return redirect(request.META.get('HTTP_REFERER', 'users'))

@login_required
def unblock_user(request, userID):
  current_user = request.user
  user_to_unblock = get_object_or_404(CustomUser, id=userID)

  if user_to_unblock != current_user:
    current_user.blocked_users.remove(user_to_unblock)
    
    request.session['modal_data'] = {
      'template': '_success_modal.html',
      'title': 'User Unblocked',
      'message': f'You have unblocked <b><u>{user_to_unblock.username}</b></u> 🔓.</br>You may now see messages from this user.'
    }

  return redirect(request.META.get('HTTP_REFERER', 'users'))
