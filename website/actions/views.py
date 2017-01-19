import json
from hashlib import sha1
import httplib2
from dateutil import parser

from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from oauth2client.contrib.django_util import decorators

from social_django.utils import psa
from social_django.models import UserSocialAuth
from social_django.views import _do_login

from .serializers import GoogleActionResponseSerializer, GoogleActionRequestSerializer
from .models import ActionLog
from .gwrapper import GWrapper


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

@psa('social:complete')
@csrf_exempt
def complete_google_action_access(request, backend):
    social = request.backend.auth_complete_code(request.POST.get('code'))
    session_state = request.backend.strategy.session_get('state')
    if social:
        _do_login(request.backend, social.user, social)
        url = '{0}?state={1}&code={2}'.format(request.POST.get('redirect_uri'),
                                              social.extra_data['state'],
                                              request.POST.get('code'))
        return HttpResponseRedirect(url)
    return HttpResponse('Failed')


@psa('social:complete')
@csrf_exempt
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    user = request.backend.auth_complete_code(request.POST.get('code'))

    if user:
        login(request, user)
        return 'OK'
    else:
        return 'ERROR'

class ActionsViewSet(viewsets.GenericViewSet):
    serializer_class = GoogleActionResponseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _get_signed_gwrapper(self, request):
        if not request.is_authenticated():
            return None

        try:
            gwrap = GWrapper.new_from_user(request.user)
            return grwrap
        except Exception as e:
            return None

    def authorization_required():
        return Response({
                    "speech": "It seems that my permission to access your calendar has expired.",
                    'displayText': 'Please visit http://home.ghoknhar.com/social/login/google-oauth2/',
                    "contextOut": [{
                        "name": "CASTILLO_OAUTH_ERROR",
                        "lifespan": 0,
                        "parameters": {
                            "url": 'http://home.ghoknhar.com/social/login/google-oauth2/'
                        }
                    }]
                })

    @list_route(methods=['POST'])
    def actions(self, request):
        try:
            result = GoogleActionRequestSerializer(request.data)
        except Exception as e:
            print str(e)
            return Response({
                'success': True
            })

        action = request.data['result']['action']
        # default response
        response = {'speech': 'I do not seem capable of handling this request.',
                    'displayText': 'Castillo did not understand the requested action. Action was {0}'.format(action)}

        if action == 'castillo.add_calendar':
            signed_gwrap = self._get_signed_gwrapper(request)
            if signed_gwrap is None:
                return self.authorization_required()

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
            success, reason = gwrap.calendar_add_event('mmdelascu@gmail.com', event)
            if success:
                response = {'speech':r, "displayText":r}
            else:
                response = {'speech': "I failed to save your calendar event. Please review your device more additional details.",
                                'displayText': reason}
            
                
            

        result_data = result.data
        ActionLog.objects.create(transaction_id=result_data['id'],
                                 session_id=result_data['sessionId'],
                                 date_created=parser.parse(result_data['timestamp']),
                                 status_code=result_data['status']['code'],
                                 fulfillment_payload=json.dumps(response),
                                 action_payload=json.dumps(request.data))
        return Response(response)
