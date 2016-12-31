import json
from hashlib import sha1

from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from django.template.loader import get_template

from .serializers import GoogleActionResponseSerializer, GoogleActionRequestSerializer

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

        response = GoogleActionResponseSerializer()
        response.add_text_response('I will add that day to your Work Schedule')

        print json.dumps(response.data)
        return Response(response.data)
