from .auth_urls import urlpatterns as auth_urls
from .profile_urls import urlpatterns as profile_urls
from .friend_urls import urlpatterns as friend_urls

urlpatterns = auth_urls + profile_urls + friend_urls
