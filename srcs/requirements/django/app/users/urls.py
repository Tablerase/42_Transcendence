from django.urls import path, include

urlpatterns = [
  path("auth/", include('users.urls.auth_urls')),
  path("profile/", include('users.urls.profile_urls')),
  path("friends/", include('users.urls.friend_urls')),
]
