

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routings
from django.core.asgi import get_asgi_application
from chat.auth_token import TokenAuthMiddleware
from channels.security.websocket import AllowedHostsOriginValidator


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social.settings')

django_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": AllowedHostsOriginValidator(TokenAuthMiddleware(
        URLRouter(
            chat.routings.websocket_urlpatterns
            )
        )
    ),
})

