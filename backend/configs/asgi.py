"""
ASGI config for configs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')
asgi_application = get_asgi_application()
from configs.routing import websocket_urlpatterns

from core.middlewares.auth_socket_middleware import AuthSocketMiddleware

application = ProtocolTypeRouter({
    'http': asgi_application,
    'websocket': AuthSocketMiddleware(URLRouter(websocket_urlpatterns))
})
