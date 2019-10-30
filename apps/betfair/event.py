"""
Competitions module
"""
import logging
import re
from apps.betfair.api.client import api_client
from apps.competition.models import Competition, Event

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
                obj, created = Event.objects.update_or_create(
                    name=event['name'],
                    competition=competition,
                    betfair_id=event['id'],
                    home=match.group(1),
                    away=match.group(2),
                    defaults={
                        'start_time': event['openDate']
                    }
                )
                if created:
                    LOG.info('created event - %s - starts %s', obj.name, obj.start_time)
                else:
                    LOG.debug('updated event - %s - starts %s', obj.name, obj.start_time)
