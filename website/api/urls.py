from django.conf.urls import include, url

from rest_framework.authtoken import views

urlpatterns = [
    url(r'^auth/token/', views.obtain_auth_token),
    url(r'^zwave/', include('website.zwave.urls')),
]
