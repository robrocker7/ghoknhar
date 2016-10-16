from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from website.zwave.models import Switch

def home(request):

    switches = Switch.objects.all()

    return render(request, 'index.html', {
            'switches': switches
        })