import json

from channels import Channel, Group
from channels.sessions import channel_session, enforce_ordering
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

from website.chat.models import Room, Message
from website.chat.serializers import MessageSerializer

@enforce_ordering(slight=True)
@channel_session
def ws_connect(message):
    prefix, slug = message['path'].strip('/').split('/')
    room, created = Room.objects.get_or_create(slug=slug)
    Group('chat-' + slug).add(message.reply_channel)
    message.channel_session['room'] = room.slug


@enforce_ordering(slight=True)
@channel_session
def ws_receive(message):
    slug = message.channel_session['room']
    print 'Message Get: {0}'.format(slug)
    room = Room.objects.get(slug=slug)
    data = json.loads(message['text'])
    m = room.messages.create(username=data['username'], message=data['message'])
    ms = MessageSerializer(m)
    Group('chat-'+slug).send({'text': json.dumps(ms.data)})

# Connected to websocket.disconnect
@enforce_ordering(slight=True)
@channel_session
def ws_disconnect(message):
    slug = message.channel_session['room']
    Group('chat-'+slug).discard(message.reply_channel)