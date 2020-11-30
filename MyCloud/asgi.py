"""
ASGI config for MyCloud project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""


import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.conf.urls import url
from django.core.asgi import get_asgi_application

from MainApp.consumers import WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyCloud.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),

    # Django's ASGI application to handle WebSocket requests
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url("ws/live-progress/", WebSocket.as_asgi()),
        ])
    ),
})
