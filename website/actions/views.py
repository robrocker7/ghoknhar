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
from .models import ActionLog, ActionDatastore
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


class ActionsViewSet(viewsets.GenericViewSet):
    serializer_class = GoogleActionResponseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _get_signed_gwrapper(self, request):
        print request.user
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

    @list_route(methods=['GET'])
    def self(self, request):
        user = None
        if request.user:
            user = request.user.email
        return Response({
                'user': user
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

        def send_response(speech, displayText, data=None):
            r = {'speech':speech, "displayText":displayText}
            if data is not None:
                r['data'] = data
            return Response(r)

        if action in ['castillo.add_work_day_to_default_calendar',]:
            gwrap = GWrapper.new_from_user(request.user)
            params = request.data['result']['parameters']
            date = params.get('date-time', params.get('date'))
            category = params.get('event_category')

            calendar_id = request.user.email
            try:
                event = ActionDatastore.objects.get(user=request.user,
                    key='{0}:event'.format(category))
            except ActionDatastore.DoesNotExist:
                return send_response('<speak>I could not find a calendar event for {0}. Please create one.</speak>'.format(category),
                    'Could not find event in Castillo.',
                    data={
                        'google': {
                            'expect_user_response': False,
                            'is_ssml': True,
                        }
                    })

            event_payload = event.populate_tokens(params)
            r = "Ok; I will add {0} to your {1} Schedule.".format(date, category)
            success, reason = gwrap.calendar_add_event(calendar_id, event_payload)
            if success:
                response = {'speech':r, "displayText":r}
            else:
                response = {'speech': "I failed to save your calendar event. Please review your device more additional details.",
                                'displayText': reason}
            response['payload'] = event_payload
            
        result_data = result.data
        ActionLog.objects.create(transaction_id=result_data['id'],
                                 session_id=result_data['sessionId'],
                                 date_created=parser.parse(result_data['timestamp']),
                                 status_code=result_data['status']['code'],
                                 fulfillment_payload=json.dumps(response),
                                 action_payload=json.dumps(request.data))
        return send_response(response['speech'], response['displayText'])
