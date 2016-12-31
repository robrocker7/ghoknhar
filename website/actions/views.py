import json
from hashlib import sha1

from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from django.template.loader import get_template

from .serializers import GoogleActionResponseSerializer, GoogleActionResultSerializer

class ActionsViewSet(viewsets.GenericViewSet):
    serializer_class = GoogleActionResultSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @list_route(methods=['POST'])
    def actions(self, request):
        try:
            result = GoogleActionResultSerializer(request.data)
        except Exception as e:
            print str(e)
            return Response({
                'success': True
            })

        response = GoogleActionResponseSerializer()
        response.id = result.id
        response.timestamp = result.timestamp
        response.status = result.status
        response.sessionId = result.sessionId
        response_result = result.result
        response_result.fulfillment = json.dumps({
            'speech': 'I will add that day to your Work Schedule',
            'messages': [{
                'type': 0,
                'speech': 'I will add that day to your Work Schedule'
            }]
        })
        response.result = response_result
        print response.data
        print json.dumps(response.data)
        return Response(response.data)
