"""
Constants Directory:

I will use this directory for the system to dynamically update it's knowledge
of which constants exist in the zwave system. The idea will be for the sync
command to look for a device type or command class and if it doesn't find it
append the new found item to the constants file and send a message to the admin

Goal is to make this system self sustaining!
"""

