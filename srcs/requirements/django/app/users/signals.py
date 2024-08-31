from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from users.models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
  """
  This signal handles both creation and updating of the Profile.
  It ensures that only one Profile is created per User instance.
  """
  if created:
    Profile.objects.create(user=instance)
  else:
    instance.profile.save(force_update=True)
    
@receiver(user_logged_out)
def update_last_online(sender, user, request, **kwargs):
  user.last_online = timezone.now()
  user.save(update_fields=['last_online'])
