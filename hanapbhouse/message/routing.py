from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^chat/(?P<room_name>[\w-]+)/(?P<user_id>[\w-]+)/$', consumers.MessageConsumer.as_asgi()),
]