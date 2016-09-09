# In routing.py
from channels.routing import route, include

from website.zwave.consumers import ws_message

# http_routing = [
#     route("http.request", poll_consumer, path=r"^/poll/$", method=r"^POST$"),
# ]

chat_routing = [
    route("websocket.receive", ws_message),
]

channel_routing = [
    # You can use a string import path as the first argument as well.
    include(chat_routing, path=r"^/zwave"),
]