from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("practice/", views.practice, name="practice"),
    path("init/", views.init, name="init"),
    path("init/<str:mode>/", views.init, name="init"),
    path("tournament/<int:tournament_id>/", views.tournament, name="tournament"),
    path("quit/<int:tournament_id>/", views.quit, name="quit"),
    path("settings/", views.settings, name="settings"),
    path('clear_modal_data/', views.clear_modal_data, name='clear_modal_data'),
]


# TODO (tests)
# Check quit/<id of tournament that exists but user is not in>/
