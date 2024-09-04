from django.shortcuts import render, redirect
from django.contrib.auth import logout
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(request, username=username, password=password)
      if user is not None:
        login(request, user)
        request.session['modal_data'] = {
          'template': '_success_modal.html',
          'title': 'Registration Successful!',
          'message': f'Your account has been created, <b>{username}</b>! You are now logged in.'
        }
        return redirect('home')
  else:
    form = UserRegisterForm()
  return render(request, 'users/auth/register.html', {'form': form})

@login_required
def user_logout(request):
  if request.method == "POST":
    logout(request)
    request.session['modal_data'] = {
      'template': '_success_modal.html',
      'title': 'Logged Out',
      'message': 'You have been successfully logged out.'
    }
    return render(request, 'users/auth/logout.html', {})
  else:
    return render(request, 'users/auth/logout_confirm.html', {})
