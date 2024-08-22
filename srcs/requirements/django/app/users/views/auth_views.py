from django.shortcuts import render, redirect
from django.contrib.auth import logout
from users.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Your account has been created! You can now login!')
      return redirect('login')
  else:
    form = UserRegisterForm()
  return render(request, 'users/auth/register.html', {'form': form})

@login_required
def user_logout(request):
  if request.method == "POST":
    logout(request)
    return render(request, 'users/auth/logout.html', {})
  else:
    return render(request, 'users/auth/logout_confirm.html', {})
