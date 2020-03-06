"""
Session manager
"""
import logging
import requests
from settings.base import BASE_DIR
from apps.betfair.models import BetfairSession

LOG = logging.getLogger(__name__)

LOGIN_URI = 'https://identitysso-cert.betfair.com/api/certlogin'
KEEPALIVE_URI = 'https://identitysso.betfair.com/api/keepAlive'

def login(user, passwd, app):
    """ TODO """
    payload = f'username={user}&password={passwd}'
    headers = {
        'X-Application': app,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    cert = BASE_DIR + '/settings/certs/client.crt'
    key = BASE_DIR + '/settings/certs/client.key'
    req = requests.post(LOGIN_URI, data=payload, cert=(cert, key), headers=headers)
    if req.status_code == 200 and 'sessionToken' in req.json():
        return req.json()['sessionToken']
    LOG.error('could not create session token: %s', req.json())
    return False

def keep_alive(session_token):
    """ TODO """
    headers = {
        'Accept': 'application/json',
        'X-Authentication': session_token
    }
    req = requests.get(KEEPALIVE_URI, headers=headers)
    if req.status_code == 200 and req.json()['status'] == 'SUCCESS':
        return True
    LOG.warning('token is not valid anymore, could not keepAlive')
    LOG.debug('response: %s', req.json())
    return False

def current_token():
    """ TODO """
    session = BetfairSession.objects.filter(active=True).first()
    if session:
        LOG.debug('checking if session token [%.5s] is still valid', session.session_token)
        if keep_alive(session.session_token):
            return session.session_token
        session.active =  False
        session.save()
    return False

def get_token(user, passwd, app):
    """ TODO """
    token = current_token()
    if token:
        LOG.info('existing session token is valid')
        return token
    LOG.info('creating session token')
    token = login(user, passwd, app)
    if token:
        LOG.debug('token created - %s', token)
        session = BetfairSession(session_token=token, active=True)
        session.save()
        return token
    else:
        return None
