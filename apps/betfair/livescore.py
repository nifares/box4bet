"""
LiveScore puller
"""


import logging
import re
from lxml import html
import requests
from datetime import datetime
from pytz import timezone
from apps.betfair.api.client import api_client
from apps.competition.models import Competition, Event
from django.conf import settings

LOG = logging.getLogger(__name__)

URI = 'https://betfair.com/sport/{}/event?eventId={}'

def get_raw_event(event_id, kind):
    """
    TODO
    """
    try:
        req = requests.get(URI.format(kind.lower(), event_id))
    except (ConnectionError, ConnectionResetError, TimeoutError) as error:
        LOG.error(error)
        LOG.debug(URI)
        # TODO - raise our exception here
        return None
    return html.fromstring(req.text)



def get_score(event_id):
    event = Event.objects.get(betfair_id=event_id)
    LOG.debug(f'getting livescore for event {event.name} [{event_id}]')
    score_site = get_raw_event(event.betfair_id, event.competition.kind.name)

    home_score = score_site.xpath('//span [@class="home-score ui-score-home"]/text()')[0]
    away_score = score_site.xpath('//span [@class="away-score ui-score-away"]/text()')[0]
    match_time = score_site.xpath('//span [@class="time ui-time-stop-format"]/text()')[0]

    LOG.info(f'updating livescore data - {event.home} [{home_score}:{away_score}] {event.away} ( {match_time} )')

    event.home_score = home_score
    event.away_score = away_score
    event.save()