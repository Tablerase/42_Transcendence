from django.urls import path
from users.views.friend_views import (
  users_list,
  users_search,
  view_friend_requests,
  view_friends,
)
from users.views.friend_actions_views import (
  send_friend_request,
  accept_friend_request,
  remove_friend,
  cancel_friend_request,
  reject_friend_request,
)
from users.views.block_views import (
  block_user,
  unblock_user,
)

urlpatterns = [
  path("users/", users_list, name='users'),
  path("search-users/", users_search, name='users-search'),
  path("send-friend-request/<int:userID>/", send_friend_request, name='send-friend-request'),
  path("remove-friend/<int:userID>/", remove_friend, name='remove-friend'),
  path('cancel-friend-request/<int:userID>/', cancel_friend_request, name='cancel-friend-request'),
  path("accept-friend-request/<int:requestID>/", accept_friend_request, name='accept-friend-request'),
  path('reject-friend-request/<int:requestID>/', reject_friend_request, name='reject-friend-request'),
  path("friend-requests/", view_friend_requests, name='view-friend-requests'),
  path("friends/", view_friends, name='view-friends'),
  path('block-user/<int:userID>/', block_user, name='block-user'),
  path('unblock-user/<int:userID>/', unblock_user, name='unblock-user'),
]
