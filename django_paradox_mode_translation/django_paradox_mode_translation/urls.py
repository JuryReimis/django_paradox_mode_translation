"""django_paradox_mode_translation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django_paradox_mode_translation import settings

urlpatterns = [
    path('', include('translators_hub.urls'), name='home'),
    path('teams/', include('teams.urls'), name='teams'),
    path('moderators/', include('moderators.urls'), name='moderators'),
    path('chats/', include('chats.urls'), name='chats'),
    path('admin/', admin.site.urls),

]

if settings.DEBUG is True:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
