from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

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