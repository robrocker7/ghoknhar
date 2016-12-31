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
        print request.data
        try:
            result = GoogleActionResultSerializer(request.data)
        except Exception as e:
            print str(e)
        result = request.data['result']
        params = result['parameters']
        action = result['action']
        id = request.data['id']
        status = request.data['status']

        return Response({
            'success': True
        })
