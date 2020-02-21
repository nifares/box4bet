"""
Competitions module
"""
import logging
import re
from datetime import datetime
from pytz import timezone
from apps.betfair.api.client import api_client
from apps.competition.models import Competition, Event
from django.conf import settings

LOG = logging.getLogger(__name__)

def get_events():
    """
    todo
    """
    api = api_client()
    regex = re.compile(r'(.*) v (.*)')
    for competition in Competition.objects.filter(enabled=True):
        events = api.list_events([competition.betfair_id])
        for event in events:
            event = event['event']
            match = regex.match(event['name'])
            if match:
                locked, start_time = parse_time(event['openDate'])
                obj, created = Event.objects.update_or_create(
                    name=event['name'],
                    competition=competition,
                    betfair_id=event['id'],
                    home=match.group(1),
                    away=match.group(2),
                    defaults={
                        'start_time': start_time,
                        'locked': locked
                    }
                )
                if created:
                    LOG.info('created event - %s - starts %s [locked: %s]', obj.name, obj.start_time, obj.locked)
                else:
                    LOG.debug('updated event - %s - starts %s [locked: %s]', obj.name, obj.start_time, obj.locked)


def parse_time(open_date):
    """
    by default timezone for openDate is GMT
    """
    start_time = datetime.strptime(
        open_date.split('.')[0],
            '%Y-%m-%dT%H:%M:%S').replace(
                tzinfo=timezone('GMT')
            )

    now = datetime.now(tz=timezone('GMT'))
    minutes_to_start = int((start_time - now).total_seconds() / 60)
    if minutes_to_start <= settings.LOCK_BEFORE:
        locked = True
    else:
        locked = False

    return locked, start_time
