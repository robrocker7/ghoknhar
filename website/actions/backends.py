from social_core.backends.google import GooglePlusAuth
from social_django.models import UserSocialAuth


class GooglePlusActionAuth(GooglePlusAuth):
    name = 'google-plus-action'
    DEFAULT_SCOPE = [
        'https://www.googleapis.com/auth/plus.login',
        'https://www.googleapis.com/auth/plus.me'
    ]

    def auth_complete_code(self, code):
        return UserSocialAuth.get_social_auth(self.name, code)