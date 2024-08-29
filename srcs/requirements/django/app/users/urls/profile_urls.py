from django.urls import path
from users.views.profile_views import (
  profile,
  profile_by_nickname,
  profile_edit,
)
from users.views.match_views import (
  match_detail_view,
)

urlpatterns = [
  path("profile/", profile, name='profile'),
  path("profile/<str:nickname>/", profile_by_nickname, name='profile-by-nickname'),
  path("edit-user-info/", profile_edit, name='profile-edit'),
  path('match-detail/<int:match_id>/', match_detail_view, name='match-detail'),
]
