import logging

from django.core.management.base import BaseCommand, CommandError
from website.places.models import PlaceMonitor

class Command(BaseCommand):
    help = 'Run latest place monitor.'

    def handle(self, *args, **options):
        try:
            pm = PlaceMonitor.objects.latest('pk')
            pm.fetch_result()
        except Exception as e:
            logging.exception(e)
            raise CommandError('Failed to Exec: {0}'.format(str(e)))
