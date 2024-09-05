from django.shortcuts import render, redirect, get_object_or_404
from users.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from users.utils import generate_dummy_matches
from users.models.User_model import CustomUser

@login_required
def profile_edit(request):
  if request.method == 'POST':
    u_form = UserUpdateForm(
      request.POST,
      instance=request.user
    )
    p_form = ProfileUpdateForm(
      request.POST,
      request.FILES,
      instance=request.user.profile
    )
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      request.session['modal_data'] = {
        'template': '_success_modal.html',
        'title': 'Profile updated',
        'message': 'Changes have been saved. Looking sexy 😏'
      }
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
  user_profile.profile.refresh_from_db()

  dummy_matches = generate_dummy_matches(user_profile)

  context = {
    'user': user_profile,
    'matches': dummy_matches,
  }

  return render(request, 'users/profile/profile.html', context)
