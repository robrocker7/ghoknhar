from django.conf.urls import url
from rest_framework import routers

from website.actions.views import ActionsViewSet
from website.actions.views import auth_start, register_by_access_token

router = routers.DefaultRouter()
router.register(r'actions', ActionsViewSet, 'actions')

urlpatterns = router.urls
urlpatterns += [
    url(r'^oauth/start/$', auth_start, name='oauthstart'),
    url(r'^oauth/token/$', register_by_access_token, name='oauthtoken'),
]
