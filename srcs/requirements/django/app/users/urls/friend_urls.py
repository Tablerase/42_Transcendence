from django.urls import path
from users.views.friend_views import (
  users_list,
  users_search,
  send_friend_request,
  accept_friend_request,
  remove_friend,
  view_friend_requests,
  view_friends,
  cancel_friend_request,
)


urlpatterns = [
  path("users/", users_list, name='users'),
  path("search_users/", users_search, name='users-search'),
  path("send_friend_request/<int:userID>/", send_friend_request, name='send-friend-request'),
  path("accept_friend_request/<int:requestID>/", accept_friend_request, name='accept-friend-request'),
  path("remove-friend/<int:userID>/", remove_friend, name='remove-friend'),
  path('cancel-friend-request/<int:user_id>/', cancel_friend_request, name='cancel_friend_request'),
  path("friend-requests/", view_friend_requests, name='view-friend-requests'),
  path("friends/", view_friends, name='view-friends'),
]
