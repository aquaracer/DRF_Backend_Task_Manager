import django, jwt, os
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.db import close_old_connections
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

ALGORITHM = "HS256"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


@database_sync_to_async
def get_user(token):
    """Получение обьекта пользователя"""

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    except:
        return AnonymousUser()

    token_exp = datetime.fromtimestamp(payload['exp'])

    if token_exp < datetime.utcnow():
        return AnonymousUser()

    try:
        user = User.objects.get(id=payload['user_id'])
    except User.DoesNotExist:
        return AnonymousUser()

    return user


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None

        scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
