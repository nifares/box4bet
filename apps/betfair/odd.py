"""
Odd jobs
"""
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from apps.betfair.api.client import api_client
from apps.box4bet.models import Competition, Event, Odd, Score

LOG = logging.getLogger(__name__)

def get_odds():
    """
    TODO
    """
    api = api_client()
    event_list = get_event_list(api)
    if event_list:
        odds_list = fetch_odds(api, event_list)
        count = 0
        for event_id, event in event_list.items():
            try:
                obj = Event.objects.get(betfair_id=event_id)
                for odd in event['odds']:
                    odd_obj, created = Odd.objects.update_or_create(
                        event=obj,
                        betfair_id=odd['selectionId'],
                        defaults={
                            'prize': odds_list[odd['marketId']][odd['selectionId']],
                            'name': name_odd(obj, odd['runnerName']),
                            'betfair_name': odd['runnerName']
                        }
                    )
                    action = 'created' if created else 'updated'
                    count += 1
                    LOG.debug('%s odds for [%s] %s event - %s [%s]',
                              action,
                              obj.betfair_id,
                              obj.name,
                              odd_obj.prize,
                              odd_obj.name)
            except ObjectDoesNotExist:
                LOG.error('event with betfair_id=%s does not exist in database', event_id)
        LOG.info('updated/created %d odds', count)
    else:
        LOG.info('no events to fetch odds for')

def get_event_list(api):
    """
    Go through all events in database to fetach their markets
    return parsed event list with details
    """
    event_ids = list(x.betfair_id for x in Event.objects.filter(locked=False).all())
    if event_ids:
        markets = api.list_market_catalogue(event_ids, len(event_ids)*2)
        return parse_markets(markets)
    return None

def parse_markets(markets):
    """
    reshape markets object to make it way easier
    to work through
    returns: dict
    """
    event_list = dict()
    for market in markets:
        odds = list()
        for odd in market['runners']:
            odds.append({
                'marketId': market['marketId'],
                'selectionId': odd['selectionId'],
                'runnerName': odd['runnerName'],
                'prize': None,
            })
        try:
            event_list[market['event']['id']]['odds'] += odds
        except KeyError:
            event_list[market['event']['id']] = {
                'name': market['event']['name'],
                'odds': odds
            }
    return event_list

def fetch_odds(api, event_list):
    """
    sadsdas
    """
    market_ids = list()
    for event in event_list.values():
        market_ids += list(set(x['marketId'] for x in event['odds']))
    market_book = api.list_market_book(market_ids)
    return parse_market_book(market_book)

def parse_market_book(market_book):
    """
    sadsdasd
    """
    parsed = dict()
    price = 'lastPriceTraded'
    for book in market_book:
        parsed[book['marketId']] = {
            x['selectionId']: x[price] if price in x else None for x in book['runners']
        }
    return parsed

def name_odd(event, name):
    """
    asdasda
    """
    translate = {
        'Home or Away': f'{event.home} or {event.away}',
        'Home or Draw': f'{event.home} or Draw',
        'The Draw': 'Draw',
        'Draw or Away': f'Draw or {event.away}'
    }

    try:
        return translate[name]
    except KeyError:
        return name

def decide_winners():
    for event in Event.objects.filter(finished=True).all():
        winners = None
        #draw
        if event.home_score_90 == event.away_score_90:
            winners = ['Draw', f'{event.home} or Draw', f'Draw or {event.away}']
        #home
        elif event.home_score_90 > event.away_score_90:
            winners = [event.home, f'{event.home} or Draw', f'{event.home} or {event.away}']
        #away
        elif event.home_score_90 < event.away_score_90:
            winners = [event.away, f'Draw or {event.away}', f'{event.home} or {event.away}']

        LOG.debug(f'winners for event {event.name} are {winners}')

        for odd in event.odd_set.all():
            if odd.name in winners:
                odd.winner = True
                odd.save()


def calculate_score():
    c = Competition.objects.get(name='UEFA Euro 2020')
    for user in User.objects.all():
        score = 0
        for bet in user.bet_set.all():
            if bet.odd.winner:
                score += bet.odd.prize
        obj, created = Score.objects.update_or_create(
            user = user,
            competition = c,
            defaults = {
                'score': round(score, 2)
            }
        )
