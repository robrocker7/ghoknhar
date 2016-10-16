import json

from channels import Channel, Group

from website.zwave.models import Switch


def ws_add(message):
    Group("zwave").add(message.reply_channel)
    print "client connect"

def ws_disconnect(message):
    Group("zwave").discard(message.reply_channel)
    print "client disconnect"