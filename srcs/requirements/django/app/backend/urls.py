import django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

django.setup()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("game/", include('game.urls')),
    path("", include('users.urls')),
    path("", RedirectView.as_view(url='game/home/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
