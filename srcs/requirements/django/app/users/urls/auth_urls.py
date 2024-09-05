from django.urls import path
from django.contrib.auth import views as auth_views
from users.views.auth_views import (
  register,
  user_logout,
  CustomLoginView,
)
from users.views.callback_views import (
  dashboard
)

urlpatterns = [
  path("register/", register, name='register'),
  path("login/", CustomLoginView.as_view(), name='login'),
  path("logout/", user_logout, name='logout'),
  path('dashboard/', dashboard, name='dashboard'),
]
