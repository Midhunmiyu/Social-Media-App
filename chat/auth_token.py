from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model


User = get_user_model()


@database_sync_to_async
def get_user(scope):
    try:
        token_key = parse_qs(scope['query_string'].decode('utf-8'))['token'][0]
        # print(token_key,'token_key1')
        token_key = token_key.replace("bearer ", "").strip() 
        # print(token_key,'token_key2')
        decoded_token = AccessToken(token_key)
        # print(decoded_token,'decoded_token')
        user_id = decoded_token['user_id']
        # print(user_id,'user_id')
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()
    except KeyError:
        return AnonymousUser()
    except Exception:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        scope['user'] = await get_user(scope)
        return await self.inner(scope, receive, send)
