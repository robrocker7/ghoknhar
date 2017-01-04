import json
from hashlib import sha1
import httplib2
from dateutil import parser

from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

from oauth2client.contrib.django_util import decorators
from oauth2client.client import AccessTokenCredentials
from social_django.models import UserSocialAuth

from .serializers import GoogleActionResponseSerializer, GoogleActionRequestSerializer
from .models import ActionLog

@decorators.oauth_enabled(scopes=['https://www.googleapis.com/auth/calendar',])
def auth_start(request):
    if request.oauth.has_credentials():
        # this could be passed into a view
        # request.oauth.http is also initialized
        #resp, content = request.oauth.http.request(
        #        'https://www.googleapis.com/calendar/v3/users/me/calendarList')

        return HttpResponse('User email: {}'.format(
            request.oauth.credentials.id_token['email']))
    else:
        return HttpResponse(
            'Here is an OAuth Authorize link:<a href="{}">Authorize</a>'
            .format(request.oauth.get_authorize_redirect()))


class ActionsViewSet(viewsets.GenericViewSet):
    serializer_class = GoogleActionResponseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @list_route(methods=['POST'])
    def actions(self, request):
        try:
            result = GoogleActionRequestSerializer(request.data)
        except Exception as e:
            print str(e)
            return Response({
                'success': True
            })



        params = request.data['result']['parameters']
        date = params.get('date-time', params.get('date'))
        r = "Ok; I will add {0} to your Work Schedule.".format(date)
        event = {
          'summary': 'Work',
          'location': '11113 Research Blvd, Austin Tx, 78759',
          'description': 'Melisa works for 12 hours',
          'start': {
            'dateTime': '{0}T06:45:00'.format(date),
            'timeZone': 'America/Chicago',
          },
          'end': {
            'dateTime': '{0}T19:15:00'.format(date),
            'timeZone': 'America/Chicago',
          },
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'popup', 'minutes': 20},
            ],
          },
        }
        try:
            u = UserSocialAuth.objects.get(uid='robrocker7@gmail.com',
                                           provider='google-oauth2')
            credentials = AccessTokenCredentials(u.extra_data['access_token'],
                'JohnsonCastillo/1.0')
            http = httplib2.Http()
            http = credentials.authorize(http)

            resp, content = http.request(
                'https://www.googleapis.com/calendar/v3/calendars/mmdelascu@gmail.com/events',
                method='POST',
                body=json.dumps(event),
                headers={'Content-Type':'application/json'})
            response = {'speech':r, "displayText":r}
        except Exception as e:
            response = {
                "speech": "It seems that my permission to access your calendar has expired.",
                'displayText': 'Please visit http://home.ghoknhar.com/social/login/google-oauth2/',
                "contextOut": [{
                    "name": "CASTILLO_OAUTH_ERROR",
                    "lifespan": 0,
                    "parameters": {
                        "url": 'http://home.ghoknhar.com/social/login/google-oauth2/'
                    }
                }]
            }

        result_data = result.data
        ActionLog.objects.create(transaction_id=result_data['id'],
                                 session_id=result_data['sessionId'],
                                 date_created=parser.parse(result_data['timestamp']),
                                 status_code=result_data['status.code'],
                                 fulfillment_payload=json.dumps(response),
                                 action_payload=json.dumps(request.data))
        return Response(response)
