
from rest_framework import generics
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework.views import Response

from .serializers import UserSerializer
from .authenticators import QuietBasicAuthentication


class AuthView(generics.GenericAPIView):
    queryset = User.objects.all()
    # authentication_classes = (QuietBasicAuthentication,)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return Response({'error': 'Not Authenicated'}, status=404)
        return Response(UserSerializer(request.user).data)

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(UserSerializer(request.user).data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({})
