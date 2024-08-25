from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include('users.urls')),
    path("users/", include('chat.urls')),
    path("game/", include('game.urls')),
    path("test/", include('test.urls')),
    path("", RedirectView.as_view(url='game/home/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
