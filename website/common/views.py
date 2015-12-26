import os

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.conf import settings

from .forms import LoginForm


def home(request):
    """ Home page of Dashboard. """
    return render(request, 'base.html', {})


def angular_template(request, path):
    """ Return HTML for Angular Templates. """
    f = open(os.path.join(settings.BASE_DIR,
                          'templates',
                          'angular',
                          'views',
                          '{0}.html'.format(path)), 'rb')
    return HttpResponse(f.read())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('common:login'))


def login_view(request):
    """ Redirect to Angular Login. """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('common:home'))
    else:
        form = LoginForm()
    return render(request, 'login.html', {
            'form': form,
        })

