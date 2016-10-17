from rest_framework import routers

from website.zwave.views import SwitchViewSet


router = routers.DefaultRouter()
router.register(r'zwave', SwitchViewSet, 'zwave')

urlpatterns = router.urls