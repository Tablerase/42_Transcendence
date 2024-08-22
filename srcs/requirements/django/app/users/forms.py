from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()
  username = forms.CharField(max_length=9)
  
  class Meta:
    model = CustomUser
    fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField()
  username = forms.CharField(max_length=9)
  
  class Meta:
    model = CustomUser
    fields = ['username', 'email']
    
class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['image']