""" TODO """
import logging
import json
import requests
from apps.competition.betfair import session

LOG = logging.getLogger('betfair.api')
API_URI = 'https://api.betfair.com/exchange/betting/rest/v1.0/'

class BetfairApi(object):
    """ TODO """
    def __init__(self, app, app_key, user, password):
        """ init """
        self.app_key = app_key
        self.session_token = session.get_token(user, password, app)


    def call(self, endpoint, payload='{"filter": {}}'):
        """TODO"""
        uri = API_URI + endpoint
        headers = {
            'X-Application': self.app_key,
            'X-Authentication': self.session_token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        LOG.debug('about to POST: %s [%s]', uri, payload)
        req = requests.post(uri, headers=headers, data=payload)
        if req.status_code == 200:
            return req.json()

    def list_event_types(self):
        """TODO"""
        return self.call('listEventTypes/')

    def list_competitions(self, event_type):
        """TODO"""
        payload = {
            'filter': {
                'EventTypeIds': event_type
            }
        }
        return self.call('listCompetitions/', json.dumps(payload))

    def list_events(self, competition_id):
        """TODO"""
        payload = {
            'filter': {
                'CompetitionIds': competition_id
            }
        }
        print(payload)
        return self.call('listEvents/', json.dumps(payload))
