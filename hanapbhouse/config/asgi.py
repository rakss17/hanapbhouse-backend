import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from config.auth_middleware import JwtAuthMiddlewareStack
import api.routing
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': JwtAuthMiddlewareStack(
        URLRouter(
            [re_path(r'ws/', URLRouter(api.routing.websocket_urlpatterns))]
        )
    ),
})