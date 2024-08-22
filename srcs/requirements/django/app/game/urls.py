from django.urls import path

from . import views

urlpatterns = [
    path("pong/", views.pong, name="pong"),
    path("home/", views.home, name="home"),
    path("init/", views.init, name="init"),
    path("init/<str:mode>/", views.init, name="init"),
    path("lobby/<int:id>/", views.lobby, name="lobby"),
    path("quit/<int:id>/", views.quit, name="quit"),
    path("start/<int:id>/", views.start, name="start"),
]