from django.urls import path
from django.contrib.auth import views as auth_views
from users.views.auth_views import (
  register,
  user_logout,
)

urlpatterns = [
  path("register/", register, name='register'),
  path("login/", auth_views.LoginView.as_view(template_name='users/auth/login.html'), name='login'),
  path("logout/", user_logout, name='logout'),
]
