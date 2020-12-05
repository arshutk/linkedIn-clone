"""
ASGI config for linkedin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
from channels.auth import AuthMiddlewareStack

from channels.routing import ProtocolTypeRouter, URLRouter


# from django.core.asgi import get_asgi_application

from chat import routing

from django.core.asgi import get_asgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linkedin.settings")

application = ProtocolTypeRouter({

    # http urls are automatically routed
    "http": get_asgi_application(),
    
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})