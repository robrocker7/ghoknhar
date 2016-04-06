import json
import requests
import twilio
import twilio.rest
from dateutil.relativedelta import relativedelta

from django.conf import settings


def fetch_directions_from_google(start, end, avoidance=None, arrival_time=None, departure_time='now'):
    google_url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': start.address,
        'destination': end.address,
        'avoid': avoidance,
        'arrival_time': arrival_time,
        'departure_time': departure_time,
        'key': settings.GOOGLE_DIRECTIONS_TOKEN,
    }

    payload = requests.get(settings.GOOGLE_DIRECTIONS_URL, params=params)
    print payload.url
    return payload.json()


def parse_directions(directions):
    routes = directions['routes']
    results = []
    for route in routes:
        summary = route['summary']
        bounds = get_bounds_from_google_route(route)
        legs = get_legs_from_google_route(route)
        try:
            leg = legs[0]
        except IndexError:
            raise Exception('Expected list')

        results.append({
            'summary': summary,
            'bounds': bounds,
            'start_address': leg['start_address'],
            'start_location': leg['start_location'],
            'end_address': leg['end_address'],
            'end_location': leg['end_location'],
            'distance': leg['distance'],
            'duration': leg['duration'],
            'steps': json.dumps(leg['steps'])
        })
    return results


def get_bounds_from_google_route(route):
    bound = route['bounds']
    return ('{0},{1}'.format(bound['northeast']['lat'],
                             bound['northeast']['lng']),
            '{0},{1}'.format(bound['southwest']['lat'],
                             bound['southwest']['lng']),)


def get_legs_from_google_route(route):
    legs = route['legs']
    results = []
    for leg in legs:

        ctx = {
            'distance': leg['distance']['value'],
            'duration': leg['duration']['value'],
            'start_address': leg['start_address'],
            'end_address': leg['end_address'],
            'start_location': leg['start_location'],
            'end_location': leg['end_location'],
            'steps': []
        }

        for step in leg['steps']:
            ctx['steps'].append({
                'distance': step['distance']['value'],
                'duration': step['duration']['value'],
                'start_location': step['start_location'],
                'end_location': step['end_location'],
                'mode': step['travel_mode'],
                'summary': step['html_instructions']
            })

        results.append(ctx)
    return results


def send_twilio_message(message, to="5125224361"):
    try:
        client = twilio.rest.TwilioRestClient(settings.TWILIO_SID,
                                              settings.TWILIO_TOKEN)
        message = client.messages.create(
            body=message,
            to="+1{0}".format(to),
            from_="+17377779904"
        )
    except twilio.TwilioRestException as e:
        print e

def human_readable_duration(duration):
    attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
    human_readable = lambda delta: ['%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1]) for attr in attrs if getattr(delta, attr)]
    return human_readable(relativedelta(seconds=duration))