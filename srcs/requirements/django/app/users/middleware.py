from django.utils import timezone
from django.conf import settings

class UpdateLastOnlineMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)

    if request.user.is_authenticated:
      request.user.last_online = timezone.now()
      request.user.save(update_fields=['last_online'])

    return response