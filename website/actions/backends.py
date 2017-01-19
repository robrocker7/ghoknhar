from social_core.backends.google import GooglePlusAuth


class GooglePlusActionAuth(GooglePlusAuth):
    name = 'google-plus-action'
    DEFAULT_SCOPE = [
        'https://www.googleapis.com/auth/plus.login',
        'https://www.googleapis.com/auth/plus.me'
    ]