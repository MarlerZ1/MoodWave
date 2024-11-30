import jwt
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from MoodWave import settings
from authorization.models import User


class CombinedAuthMiddleware:
    """
    Custom middleware what choose correct middleware between AuthMiddlewareStack and JwtAuthMiddlewareStack
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        for key, value in scope.get('headers', []):
            if key == b'authorization':
                print("JwtAuthMiddlewareStack was choosen")
                token = value.decode('utf-8').split('Bearer ')[-1]
                return await JwtAuthMiddleware(self.app)(scope, receive, send, token)
        else:
            print("AuthMiddlewareStack was choosen")
            return await AuthMiddlewareStack(self.app)(scope, receive, send)



class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner, *args, **kwargs):
        super().__init__(inner, *args, **kwargs)

    async def __call__(self, scope, receive, send, token):
        if token:
            try:
                payload = self.decode_jwt(token)
                user = await self.get_user(payload['user_id'])
                scope['user'] = user
            except jwt.ExpiredSignatureError as e:
                scope['user'] = AnonymousUser()
                print(e)
            except jwt.InvalidTokenError as e:
                print(e)
                scope['user'] = AnonymousUser()
        else:
            print("Where is no token")
            scope['user'] = AnonymousUser()

        await super().__call__(scope, receive, send)


    def decode_jwt(self, token):
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()