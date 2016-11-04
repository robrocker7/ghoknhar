# In routing.py
from channels.routing import route, include

from website.zwave.consumers import ws_add, ws_disconnect

# chat consumers
from website.chat.consumers import ws_connect as chat_connect
from website.chat.consumers import ws_disconnect as chat_disconnect
from website.chat.consumers import ws_receive as chat_receive

# http_routing = [
#     route("http.request", poll_consumer, path=r"^/poll/$", method=r"^POST$"),
# ]

chat_routing = [
    route("websocket.connect", chat_connect),
    route("websocket.receive", chat_receive),
    route("websocket.disconnect", chat_disconnect)
]

zwave_routing = [
    route("websocket.connect", ws_add),
    route("websocket.disconnect", ws_disconnect)
]

channel_routing = [
    # You can use a string import path as the first argument as well.
    include(zwave_routing, path=r"^/zwave"),
    include(chat_routing, path=r"^/chat"),
]