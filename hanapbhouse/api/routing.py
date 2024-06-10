from django.urls import re_path
from channels.routing import URLRouter
import message.routing


websocket_urlpatterns = [
    re_path(r'message/', URLRouter(message.routing.websocket_urlpatterns)),
]