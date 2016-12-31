from rest_framework import routers

from website.actions.views import ActionsViewSet


router = routers.DefaultRouter()
router.register(r'actions', ActionsViewSet, 'actions')

urlpatterns = router.urls
