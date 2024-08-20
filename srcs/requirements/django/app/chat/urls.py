from django.urls import path
from .views import CommentListView, CommentCreateView
from . import views
from users import views as user_views

urlpatterns = [
    path("", CommentListView.as_view(), name="chat-home"),
    path("about/", views.about, name="chat-about"),
    path("comment/new/", CommentCreateView.as_view(), name="comment-create"),
]
