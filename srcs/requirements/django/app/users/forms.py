from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models.Profile_model import Profile
from users.models.User_model import CustomUser
from users.models.Customization_model import Customization

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

class CustomizationForm(forms.ModelForm):
  class Meta:
    model = Customization
    fields = ['ball', 'paddle_color']
    widgets = {
      'ball': forms.Select(attrs={'class': 'form-control'}),
      'paddle_color': forms.Select(attrs={'class': 'form-control'}),
    }
