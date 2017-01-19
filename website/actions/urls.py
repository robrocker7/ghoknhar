from django.conf.urls import url
from rest_framework import routers

from website.actions.views import ActionsViewSet
from website.actions.views import auth_start, complete_google_action_access

router = routers.DefaultRouter()
router.register(r'actions', ActionsViewSet, 'actions')

urlpatterns = router.urls
urlpatterns += [
    url(r'^oauth/start/$', auth_start, name='oauthstart'),
    url(r'^oauth/token/(?P<backend>[^/]+)/$', complete_google_action_access, name='oauthtoken'),
]
