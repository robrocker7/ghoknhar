import json

from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination

from website.chat.serializers import RoomSerializer, MessageSerializer
from website.chat.models import Room, Message
from website.common.views import CsrfExemptSessionAuthentication

class MessagePaginator(PageNumberPagination):
    page_size = 30
    max_page_size = 100

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_object(self, slug=None):
        if slug is None:
            slug = self.kwargs.get('slug')

        # GET OR CREATE FROM PUT
        if self.request.method == 'PUT':
            obj, created = Room.objects.get_or_create(slug=slug)
            return obj
        else:
            return super(RoomViewSet, self).get_object()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePaginator

    @list_route(methods=['GET'])
    def room(self, request, slug):
        messages = MessageSerializer(self.get_queryset().filter(room__slug=slug), many=True)
        return Response({'success':True,'messages': messages.data})
