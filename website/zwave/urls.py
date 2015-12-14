from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .api import DeviceAll, DeviceView

restpatterns = [
    url(r'^device/(?P<pk>[\d]+)/$', DeviceView.as_view()),
    url(r'^device/$', DeviceAll.as_view()),
]

urlpatterns = format_suffix_patterns(restpatterns)
