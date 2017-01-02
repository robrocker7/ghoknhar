"""ghokmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import oauth2client.contrib.django_util.site as django_util_site

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('website.zwave.urls', namespace='zwave')),
    url(r'^api/', include('website.chat.urls', namespace='chat')),
    url(r'^api/', include('website.actions.urls', namespace='actions')),
    url(r'^oauth2/', include(django_util_site.urls)),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('website.common.urls', namespace='common')),
]
