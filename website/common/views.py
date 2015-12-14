from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from .forms import LoginForm

# @login_required
def home(request):
    """ Home page of Dashboard. """
    return render(request, 'index.html', {})


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

