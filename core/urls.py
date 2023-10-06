from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apps.home.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('client/', include('apps.client.urls')),
]

urlpatterns_django_debug_toobar = [
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += urlpatterns_django_debug_toobar
