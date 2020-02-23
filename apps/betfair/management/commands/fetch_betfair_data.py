from apps.betfair.event import get_events
from apps.betfair.odd import get_odds
from apps.betfair.competition import get_competition_kinds, get_competitions
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'kurwoooo'

    def handle(self, *args, **kwargs):
        get_competition_kinds()
        get_competitions()
        get_events()
        get_odds()