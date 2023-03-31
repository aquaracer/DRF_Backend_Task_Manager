from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from datetime import timedelta, datetime
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt

from .models import User
from .serializers import GoogleAuthSerializer


def create_token(user_id: int) -> dict:
    """ Создание токена
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'user_id': user_id,
        'access_token': create_access_token(
            data={'user_id': user_id}, expires_delta=access_token_expires
        ),
        'token_type': 'Token'
    }


def create_access_token(data: dict, expires_delta: timedelta = None):
    """ Создание access token
    """
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire, 'sub': 'access'})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def check_google_auth(google_user: GoogleAuthSerializer) -> dict:
    try:
        id_token.verify_oauth2_token(
            google_user['token'], requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise AuthenticationFailed(code=403, detail='Bad token Google')

    user, _ = User.objects.get_or_create(username=google_user['email'])
    return create_token(user.id)