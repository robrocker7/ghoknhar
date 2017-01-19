from social_core.backends.google import GooglePlusAuth


class GooglePlusActionAuth(GooglePlusAuth):
    name = 'google-plus-action'
    DEFAULT_SCOPE = [
        'https://www.googleapis.com/auth/plus.login',
        'https://www.googleapis.com/auth/plus.me',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]

    def user_data(self, access_token, *args, **kwaargs):
        """Return user data from Google API"""
        print access_token
        return self.get_json(
            'https://www.googleapis.com/plus/v1/people/me',
            params={
                'access_token': access_token,
                'alt': 'json'
            }
        