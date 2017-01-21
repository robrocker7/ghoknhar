import logging
import httplib2
import json

from social_django.models import UserSocialAuth
from oauth2client.client import AccessTokenCredentials, AccessTokenCredentialsError

from .serializers import GoogleCalendar
from .models import ActionDatastore

class GWrapper(object):
    HTTP = None
    CREDENTIALS = None
    BASE_URL = 'https://www.googleapis.com'
    
    @classmethod
    def new_from_access_token(cls, access_token):
        try:
            credentials = AccessTokenCredentials(access_token, 'JohnsonCastillo/1.0')
            http = httplib2.Http()
            http = credentials.authorize(http)
        except AccessTokenCredentialsError as e:
            logging.error(str(e))
            logging.stacktrace(e)
            return None
        return cls(http, credentials)

    @classmethod
    def new_from_user(cls, user):
        users = UserSocialAuth.objects.filter(user=user, provider='google-plus-action')
        for user in users:
            gwrap = cls.new_from_access_token(user.extra_data['access_token'])
            if gwrap is not None:
                return gwrap
        return None

    @staticmethod
    def validate_response(resp):
        #TODO: expand upon this
        if str(getattr(resp, 'status'))[0] == '2':
            return True
        return False

    @staticmethod
    def error_response(resp):
        return False, resp.reason

    @staticmethod
    def success_response(resp):
        return True, resp

    def _request(self, url, method='GET', body={}):
        url = self.BASE_URL + url
        if method == 'GET':
            return self.HTTP.request(url, method='GET',
                headers={'Content-Type':'application/json'})
        elif method == 'POST':
            return self.HTTP.request(
                url, method='POST', body=json.dumps(body),
                headers={'Content-Type':'application/json'})
        raise NotImplemented('Only GET and POST are implemeted.')

    def datastore_get(self, key):
        pass

    def calendar_fetch_all(self):
        resp, content = self._request('/calendar/v3/users/me/calendarList', method='GET')
        if not GWrapper.validate_response(resp):
            return GWrapper.error_response(resp)

        json_content = json.loads(content)

        calendars = []
        for item in json_content['items']:
            calendars.append(GoogleCalendar(item).data)

        return GWrapper.success_response(calendars)


    def calendar_add_event(self, calendar_id, event):
        resp, content = self._request('/calendar/v3/calendars/{0}/events'.format(calendar_id),
            method='POST', body=json.dumps(event))

        if not GWrapper.validate_response(resp):
            return GWrapper.error_response(resp)
        return GWrapper.success_response(None)

    def __init__(self, http, credentials):
        self.HTTP = http
        self.CREDENTIALS = credentials
