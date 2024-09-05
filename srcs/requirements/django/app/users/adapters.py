from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from users.models.Profile_model import Profile

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(MySocialAccountAdapter, self).save_user(request, sociallogin, form)
        extra_data = sociallogin.account.extra_data
        
        if 'email' in extra_data:
            user.email = extra_data.get('email')
            user.save()

        profile, created = Profile.objects.get_or_create(user=user)
