from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", views.home, name="home"),
]

# Uploaded photos. For a real production server, let nginx/Apache serve MEDIA_ROOT instead.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
