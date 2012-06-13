# Import Django settings for web project.
import sys
import os

# settings.py is in PROJECT_ROOT/src; hence, PROJECT_ROOT is '../'
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Our per-deployment settings reside in a `django` package in
# PROJECT_ROOT/etc/
sys.path.insert(1, PROJECT_ROOT)

# etc.django.common will export default settings,
# and it will attempt to override those defaults by importing etc.django.local,
# which could be a symbolic link to your custom, version-controlled settings.
from etc.django.common import *
