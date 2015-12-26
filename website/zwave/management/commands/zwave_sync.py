import logging

from django.core.management.base import BaseCommand, CommandError
from website.zwave.models import Device

class Command(BaseCommand):
    help = 'Syncs Database with latest ZWave Controller Data'

    def handle(self, *args, **options):
        try:
            Device.objects.sync_data()
        except Exception as e:
            logging.exception(e)
            raise CommandError('Failed to Sync: {0}'.format(str(e)))
