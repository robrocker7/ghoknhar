import json
from hashlib import sha1

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

from .serializers import GoogleActionResponseSerializer, GoogleActionRequestSerializer


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

    @decorators.oauth_enabled(scopes=['https://www.googleapis.com/auth/calendar',])
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

        resp, content = request.oauth.http.request(
            'https://www.googleapis.com/calendar/v3/calendars/mmdelascu@gmail.com/events',
            method='POST',
            body=json.dumps(event),
            headers={'Content-Type':'application/json'})
        return Response({'speech':r, "displayText":r})
