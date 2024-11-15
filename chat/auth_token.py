import jwt
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.conf import settings
import logging
from channels.db import database_sync_to_async


from user.models import CustomUser

logger = logging.getLogger(__name__)

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        user = AnonymousUser()  # Default to AnonymousUser
        
        if b'authorization' in headers:
            try:
                # Extract token from 'Authorization: Bearer <token>'
                authorization_header = headers[b'authorization'].decode()
                token_name, token_key = authorization_header.split()

                if token_name.lower() == 'bearer':  # Ensure token format is Bearer
                    # Decode and validate the token using SimpleJWT
                    try:
                        # Decode the token
                        payload = jwt.decode(token_key, settings.SECRET_KEY, algorithms=['HS256'])
                        # Get the user ID from the payload and fetch the user
                        user_id = payload.get('user_id')
                        user = await database_sync_to_async(CustomUser.objects.get)(id=user_id)
                        logger.info(f"Authenticated user: {user.username}")
                    except (InvalidToken, TokenError) as e:
                        logger.error(f"Invalid token: {e}")
                        user = AnonymousUser()  # Invalid token, fall back to AnonymousUser
            except ValueError:
                logger.error("Authorization header is not in Bearer format.")
        
        # Set the user in the scope
        scope['user'] = user

        # Pass the scope to the next layer
        return await self.inner(scope, receive, send)

# Wrapper to apply this middleware stack
TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
