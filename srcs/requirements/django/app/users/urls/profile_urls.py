from django.urls import path
from users.views.profile_views import (
  profile,
  profile_by_nickname,
  profile_edit,
)

urlpatterns = [
  path("profile/", profile, name='profile'),
  path("profile/<str:nickname>/", profile_by_nickname, name='profile-by-nickname'),
  path("edit-user-info/", profile_edit, name='profile-edit'),
]
