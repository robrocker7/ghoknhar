# In routing.py
from channels.routing import route, include

from website.zwave.consumers import ws_add, ws_disconnect

# http_routing = [
#     route("http.request", poll_consumer, path=r"^/poll/$", method=r"^POST$"),
# ]

chat_routing = [
    route("websocket.connect", ws_add),
    route("websocket.disconnect", ws_disconnect)
]

channel_routing = [
    # You can use a string import path as the first argument as well.
    include(chat_routing, path=r"^/zwave"),
]