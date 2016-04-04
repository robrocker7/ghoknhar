import logging

from django.core.management.base import BaseCommand, CommandError
from website.places.models import MonitorFrequency

class Command(BaseCommand):
    help = 'Run crons.'

    def handle(self, *args, **options):
        try:
            monitors = MonitorFrequency.valid_crons()
            print monitors
            for monitor in monitors:
                monitor.fetch_result()
        except Exception as e:
            logging.exception(e)
            raise CommandError('Failed to Exec: {0}'.format(str(e)))
