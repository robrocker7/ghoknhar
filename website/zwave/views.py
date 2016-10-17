import json

from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from website.zwave.serializers import SwitchSerializer
from website.zwave.models import Switch

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class SwitchViewSet(viewsets.ModelViewSet):
    queryset = Switch.objects.all()
    serializer_class = SwitchSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_object(self, device_id=None):
        if device_id is None:
            device_id = self.kwargs.get('pk')

        if self.request.method == 'PUT':
            obj, created = Switch.objects.get_or_create(device_id=device_id)
            return obj
        else:
            return super(SwitchViewSet, self).get_object()

    @list_route(methods=['PUT'])
    def updater(self, request):
        json_request = request.data


        device_id = json_request['device_id']
        name = json_request.get('name')

        # better logic for getting states from types
        active = json_request['types']['switch']['active']

        switch = self.get_object(device_id=int(device_id))
        if name is None and switch.name:
            name = switch.name

        switch.name = name if name is not None else 'Device {0}'.format(device_id)
        switch.device_id = device_id
        switch.active = active
        switch.save()
        return Response({'success': 'true'})