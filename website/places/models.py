import json
import logging
from croniter import croniter
from datetime import datetime, timedelta

from django.utils import timezone
from django.db import models
from django.conf import settings

from .utils import fetch_directions_from_google, parse_directions, send_twilio_message, human_readable_duration


class Place(models.Model):
    """
    Spatial object for monitoring.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class PlaceMonitor(models.Model):
    """
    Relationship for monitoring places. Caches last result.
    """
    start_location = models.ForeignKey(Place, related_name='start_location')
    end_location = models.ForeignKey(Place, related_name='end_location')
    avoidance = models.CharField(max_length=64, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    latest_result = models.IntegerField(null=True, blank=True,
                                        help_text="How long until destination; In seconds.")
    latest_result_summary = models.CharField(max_length=128,
                                             null=True, blank=True)
    latest_result_at = models.DateTimeField(null=True, blank=True)

    alert_threshold = models.IntegerField(null=True, blank=True,
                                          help_text='seconds')
    phone_number = models.CharField(max_length=10, default='5125224361')

    @property
    def latest_result_readable(self):
        """ Return human readable time. """
        read_list = human_readable_duration(self.latest_result)
        return ' '.join(read_list)

    def __unicode__(self):
        return '{0} -> {1}'.format(self.start_location.name, self.end_location.name)

    def fetch_result(self):
        """
        Recache latest result and send text if critera is met.
        """
        logging.info('Start Google Query...')
        directions = fetch_directions_from_google(self.start_location,
                                                  self.end_location,
                                                  self.avoidance)
        logging.info('Done... Writing Objects to DB...')
        results = MonitorResults.create_from_directions_call(self,
                                                             parse_directions(directions))
        fastest_results = results.monitorroute_set.get(fastest=True)

        logging.info('Done... Cached fastest result.')
        self.latest_result = fastest_results.duration
        self.latest_result_summary = fastest_results.summary
        self.latest_result_at = timezone.now()
        self.save()

        if self.latest_result <= self.alert_threshold:
            logging.info('Sending Message.')
            send_twilio_message(
                'Your route to {0} will take {1} minutes via {2}.  {3}'.format(
                    self.end_location.name,
                    self.latest_result_readable,
                    self.latest_result_summary,
                    self.end_location.address), to=self.phone_number)


class MonitorFrequency(models.Model):
    place_monitor = models.ForeignKey(PlaceMonitor)
    cron_string = models.CharField(max_length=256)

    @staticmethod
    def valid_crons():
        """ Return crons for current minute. """
        now = timezone.localtime(timezone.now())
        now = datetime(now.year, now.month, now.day, now.hour, now.minute+1)
        results = []
        for freq in MonitorFrequency.objects.all():
            icron = croniter(freq.cron_string, now)
            print icron.get_current(datetime)
            print (now - timedelta(minutes=1))
            if icron.get_prev(datetime) == (now - timedelta(minutes=1)):
                results.append(freq.place_monitor)
        return results

    def __unicode__(self):
        return '{0} @ {1}'.format(self.place_monitor,
                                  self.cron_string)


class MonitorResults(models.Model):
    """
    Log of all the requests.
    """
    place_monitor = models.ForeignKey(PlaceMonitor)
    date_created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_from_directions_call(place_monitor, directions):
        results = MonitorResults.objects.create(place_monitor=place_monitor)
        routes = [
            results.monitorroute_set.create(fastest=True, **directions[0]),
        ]
        for route in directions[1:]:
            routes.append(results.monitorroute_set.create(**route))

        return results


class MonitorRoute(models.Model):
    monitor_results = models.ForeignKey(MonitorResults)
    summary = models.CharField(max_length=128)

    distance = models.IntegerField(help_text='meters')
    duration = models.IntegerField(help_text='seconds')

    start_address = models.CharField(max_length=128)
    start_location = models.CharField(max_length=128)
    end_address = models.CharField(max_length=128)
    end_location = models.CharField(max_length=128)

    bounds = models.CharField(max_length=128)

    steps = models.TextField(null=True, blank=True,
                             help_text='JSON steps')
    fastest = models.BooleanField(db_index=True,
                                  help_text='Used to mark the fastest result.')