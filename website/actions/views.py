from hashlib import sha1

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from django.template.loader import get_template

from .serializers import GoogleActionSerializer

class ActionsViewSet(viewsets.GenericViewSet):
    serializer_class = GoogleActionSerializer

    @list_route(methods=['POST'])
    def actions(self, request):
        print request.data
        return Response({
            'success': True
        })
