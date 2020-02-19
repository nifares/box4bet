"""
Competitions module
"""
import logging
from apps.betfair.api.client import api_client
from apps.competition.models import Competition, CompetitionKind

LOG = logging.getLogger(__name__)

def get_competition_kinds():
    """
    TODO
    """
    api = api_client()
    kinds = api.list_event_types()
    for kind in kinds:
        obj, created = CompetitionKind.objects.get_or_create(
            name=kind['eventType']['name'],
            betfair_id=kind['eventType']['id'])
        if created:
            LOG.info('created competition kind - %s', obj.name)

def get_competitions():
    """
    we only do soccer at the moment
    param: list even_type_ids: get competition of given event types

    :return: list
    """
    api = api_client()
    for kind in CompetitionKind.objects.filter(enabled=True):
        LOG.info('pulling competitions of kind - %s', kind.name)
        competitions = api.list_competitions([kind.betfair_id])
        for competition in competitions:
            obj, created = Competition.objects.get_or_create(
                name=competition['competition']['name'],
                kind=kind,
                region=competition['competitionRegion'],
                betfair_id=competition['competition']['id'],
            )
            if created:
                LOG.info('created competition - %s, kind: %s, region: %s',
                         obj.name,
                         obj.kind.name,
                         obj.region)
