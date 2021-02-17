"""socialdistancework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    # Base and Home paths
    path('', include('core.urls')),
    # Contact path
    path('', include('contact.urls')),
    # Services path
    path('', include('services.urls')),
    # Celery Tasks path
    path('', include('celery_tasks.urls')),
    # IoT Module path
    path('', include('iot_module.urls')),
    # Admin path
    path('admin/', admin.site.urls),
    # Auth paths
    path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/', include('registration.urls')),
]

# Media Files for Debug Mood
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin Custom Titles
admin.site.site_header = "SOCIAL DISTANCE"
admin.site.index_title = "ADMINISTRATION PANEL"
admin.site.site_title = "SOCIAL DISTANCE"