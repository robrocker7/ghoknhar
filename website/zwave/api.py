from rest_framework import mixins
from rest_framework import generics

from .models import Device, CommandClass
from .serializers import DeviceSerializer, CommandClassSerializer

class DeviceAll(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    """ Device APIs for getting or creating a new Device. """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DeviceView(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """ Device APIs for updating or deleting a Device. """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommandClassView(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       generics.GenericAPIView):
    """ CommandClass API for updating. """
    queryset = CommandClass.objects.all()
    serializer_class = CommandClassSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
