

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routings
from django.core.asgi import get_asgi_application
from chat.auth_token import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(URLRouter(chat.routings.websocket_urlpatterns)),
})