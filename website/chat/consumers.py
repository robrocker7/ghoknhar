from channels import Channel, Group
from channels.sessions import channel_session, enforce_ordering
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

# Connected to websocket.connect
@enforce_ordering(slight=True)
@channel_session_user_from_http
def ws_connect(message):
    # Add them to the right group
    Group("chat").add(message.reply_channel)

# Connected to websocket.receive
@enforce_ordering(slight=True)
@channel_session_user
def ws_message(message):
    Group("chat").send({
        "text": message['text'],
    })

# Connected to websocket.disconnect
@enforce_ordering(slight=True)
@channel_session_user
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)``