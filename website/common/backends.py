from social_core.backends.oauth import BaseOAuth2
from social_django.models import UserSocialAuth


class NestOAuth2(BaseOAuth2):
    name = 'nest-oauth2'
    ID_KEY = 'uid'
    AUTHORIZATION_URL = 'https://home.nest.com/login/oauth2'
    ACCESS_TOKEN_URL = 'https://api.home.nest.com/oauth2/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_URI_PARAMETER_NAME = 'oauth_callback'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]
