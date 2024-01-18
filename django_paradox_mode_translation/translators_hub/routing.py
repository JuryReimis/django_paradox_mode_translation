from django.urls import re_path

from translators_hub.consumers import ProfileInfoConsumer

websocket_urlpatterns = [
    re_path('ws/(?P<user>\S+)/$', ProfileInfoConsumer.as_asgi()),
]
