from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.files.base import ContentFile
from .models import Profile
import requests
import logging

logger = logging.getLogger(__name__)

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
            logger.debug(f"Attempting to download profile picture from: {picture_url}")
            self.download_and_save_image(profile, picture_url)

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
                logger.info(f"Profile picture saved for user: {profile.user.username}")
            else:
                logger.error(f"Failed to download image. Status code: {response.status_code}")
        except Exception as e:
            logger.error(f"Error occurred while downloading image: {str(e)}")
            