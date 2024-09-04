from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.files.base import ContentFile
from .models import Profile
import requests

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(MySocialAccountAdapter, self).save_user(request, sociallogin, form)
        extra_data = sociallogin.account.extra_data
        
        if 'email' in extra_data:
            user.email = extra_data.get('email')
            user.save()

        profile, created = Profile.objects.get_or_create(user=user)
        picture_url = extra_data.get('picture')

        if picture_url:
            profile.image_url = picture_url
            profile.image = None
            profile.save(force_update=True)
        return user

    def download_and_save_image(self, profile, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                profile.image.save(
                    f"{profile.user.username}.jpg",
                    ContentFile(response.content), 
                    save=True
                )
        except Exception as e:
            pass