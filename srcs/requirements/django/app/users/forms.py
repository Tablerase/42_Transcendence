from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models.Profile_model import Profile
from users.models.User_model import CustomUser
from users.models.Customization_model import Customization
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
  usable_password = None
  
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
  image = forms.ImageField(
    label="Profile picture",
    help_text='Maximum file size allowed is 1MB'
  )

  class Meta:
    model = Profile
    fields = ['image']

class CustomizationForm(forms.ModelForm):
  class Meta:
    model = Customization
    fields = ['ball', 'paddle_color']
    widgets = {
      'ball': forms.Select(attrs={'class': 'form-control'}),
      'paddle_color': forms.Select(attrs={'class': 'form-control'}),
    }
