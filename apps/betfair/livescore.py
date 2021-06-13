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
from apps.box4bet.models import Competition, Event
from django.conf import settings

LOG = logging.getLogger(__name__)

URI = 'https://www.betfair.com/sport/{}/event?eventId={}'

def get_raw_event(event_id, kind):
    """
    TODO
    """
    try:
        req = requests.get(URI.format(kind.lower(), event_id), allow_redirects=False)
    except (ConnectionError, ConnectionResetError, TimeoutError) as error:
        LOG.error(error)
        LOG.debug(URI)
        # TODO - raise our exception here
        return None
    if req.status_code == 200:
        return html.fromstring(req.text)
    return None

def get_score(event):
    LOG.debug(f'getting livescore for event {event.name} [{event.id}]')
    score_site = get_raw_event(event.betfair_id, event.competition.kind.name)

    if score_site is not None:
        home_score = score_site.xpath('//span [@class="home-score ui-score-home"]/text()')[0]
        away_score = score_site.xpath('//span [@class="away-score ui-score-away"]/text()')[0]
        match_time = score_site.xpath('//span [@class="time ui-time-stop-format"]/text()')[0]

        LOG.info(f'updating livescore data - {event.home} [{home_score}:{away_score}] {event.away} ( {match_time} )')

        event.home_score = home_score
        event.away_score = away_score
        event.save()
    else:
        LOG.info(f'could not get livescore data for {event.name} [{event.betfair_id}]')
        LOG.info('assuming finished')
        event.home_score_90 = event.home_score
        event.away_score_90 = event.away_score
        event.finished = True
        event.live = False
        event.save()

def get_livescores():
    """
    TODO
    """
    now = datetime.now(tz=timezone('GMT'))
    events = Event.objects.filter(finished=False).filter(start_time__lt=now).all()
    for event in events:
        get_score(event)