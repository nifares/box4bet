""" TODO """
import logging
import requests
from apps.betfair import session
from apps.betfair import filters

LOG = logging.getLogger(__name__)
API_URI = 'https://api.betfair.com/exchange/betting/rest/v1.0/'

class BetfairApi(object):
    """ TODO """
    def __init__(self, app, app_key, user, password):
        """ init """
        self.app_key = app_key
        self.session_token = session.get_token(user, password, app)

    def call(self, endpoint, payload=filters.market()):
        """TODO"""
        uri = API_URI + endpoint
        headers = {
            'X-Application': self.app_key,
            'X-Authentication': self.session_token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        LOG.debug('about to POST: %s', uri)
        LOG.debug('payload: %s', payload)
        req = requests.post(uri, headers=headers, data=payload)
        if req.status_code == 200:
            return req.json()
        LOG.error('error during API call: %s', req.json())
        LOG.error('URI: %s', uri)
        LOG.error('payload: %s', payload)
        return None

    def list_event_types(self):
        """
        :return: dict
        """
        return self.call('listEventTypes/')

    def list_competitions(self, event_type_ids):
        """
        :param list event_type_ids: list of eventTypeIds.

        :return: dict
        """
        payload = filters.market(event_type_ids=event_type_ids)
        return self.call('listCompetitions/', payload)

    def list_events(self, competition_ids):
        """
        :param list competition_ids: list of competitionIds.

        :return: dict
        """
        payload = filters.market(competition_ids=competition_ids)
        return self.call('listEvents/', payload)

    def list_market_catalogue(self, event_ids):
        """
        :param list event_ids: list of eventIds.

        :return: dict
        """
        payload = filters.market(
            event_ids=event_ids,
            market_type_codes=['MATCH_ODDS', 'DOUBLE_CHANCE'],
            attributes={
                'maxResults': 2,
                'marketProjection': ['RUNNER_DESCRIPTION']
            }
        )
        return self.call('listMarketCatalogue/', payload)

    def list_market_book(self, market_ids):
        """
        :param list market_ids: list of markedIds to get marketBooks for.

        :return: dict
        """
        payload = filters.market(attributes={'marketIds': market_ids})
        return self.call('listMarketBook/', payload)
