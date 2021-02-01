from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.core.urls')),
    path('perfil/', include('apps.profiles.urls')),
    path('contribuintes/', include('apps.contribuintes.urls')),
    path('tesouraria/', include('apps.tesouraria.urls', namespace='tesouraria')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
