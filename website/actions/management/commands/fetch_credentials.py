import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Fetch Google Credentials'
    SCOPES = 'https://www.googleapis.com/auth/calendar'

    def handle(self, *args, **kwargs):
        oauth_cred_file = settings.GOOGLE_JSON_CREDS
        print oauth_cred_file
        credential_dir = os.path.join(settings.PROJECT_ROOT, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

        credential_path = os.path.join(credential_dir,
            'google_creds.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(oauth_cred_file, self.SCOPES)
            flow.user_agent = 'Johnson Castillo'
            credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + credential_path)
        else:
            print('Valid credentials')
