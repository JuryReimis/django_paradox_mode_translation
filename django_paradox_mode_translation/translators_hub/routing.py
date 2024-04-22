from django.urls import re_path

from translators_hub.consumers import ProfileInfoConsumer

websocket_urlpatterns = [
    re_path(r'ws/(?P<user>[^/]+)/$', ProfileInfoConsumer.as_asgi()),
]
