from rest_framework import routers
from django.conf.urls import url
from website.chat.views import MessageViewSet

room_messages = MessageViewSet.as_view({'get':'room'})

router = routers.DefaultRouter()
router.register(r'chat', MessageViewSet, 'chat')

urlpatterns = [
    url(r'^chat/room/(?P<slug>\w+)/$', room_messages, name='chat-room-messages'),
]