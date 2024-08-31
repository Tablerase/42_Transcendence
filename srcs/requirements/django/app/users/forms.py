from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth import get_user_model
from django.conf import settings
import os

CustomUser = get_user_model()

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
  class Meta:
    model = Profile
    fields = ['image']

  def save(self, commit=True):
    # Call the parent save method to handle any uploaded image
    profile = super().save(commit=False)

    # Define the expected image path in the /media/ root directory
    img_name = f"{profile.user.username}_profile.jpg"
    img_path = os.path.join(settings.MEDIA_ROOT, img_name)

    # Use the uploaded image if it exists; otherwise, check for a fallback
    if not self.cleaned_data.get('image') and os.path.exists(img_path):
      print(f"Existing image found: {img_path}. Setting it as the profile image.")
      profile.image.name = img_name  # Set the image field to the existing file

    if commit:
      profile.save()
    return profile