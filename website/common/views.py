from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from rest_framework.authentication import SessionAuthentication

from website.zwave.models import Switch


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


def home(request):

    switches = Switch.objects.all()
    return render(request, 'index.html', {
            'switches': switches
        })