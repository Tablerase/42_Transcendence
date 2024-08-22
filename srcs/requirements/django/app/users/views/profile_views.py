from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from users.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

CustomUser = get_user_model()

@login_required
def profile_edit(request):
  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST,
                               request.FILES,
                               instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, f'Your account has been updated!')
      return redirect('profile')
    
  else :
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)    
  
  context = {
    'u_form': u_form,
    'p_form': p_form
  }
  
  return render(request, 'users/profile/profile_edit.html', context)

@login_required
def profile(request):
    nickname = request.user.username
    return redirect('profile-by-nickname', nickname=nickname)

def profile_by_nickname(request, nickname):
  user_profile = get_object_or_404(CustomUser, username=nickname)
  context = {
    'user_profile': user_profile
  }
  return render(request, 'users/profile/profile.html', context)

# def get_user_stats(user):
#   wins = user.total_wins
#   losses = user.total_losses
  
#   if wins == 0 and losses == 0:
#     win_percentage = 50
#     loss_percentage = 50
#   else:
#     total = wins + losses
#     win_percentage = (wins / total) * 100
#     loss_percentage = (losses / total) * 100
  
#   return win_percentage, loss_percentage

# def user_profile(request, user_id):
#   user = get_object_or_404(CustomUser, id=user_id)
#   win_percentage, loss_percentage = get_user_stats(user)

#   context = {
#     'user_profile': user_profile,
#     'win_percentage': win_percentage,
#     'loss_percentage': loss_percentage,
#   }

#   return render(request, 'users/profile/profile.html', context)