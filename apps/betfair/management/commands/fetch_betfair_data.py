from apps.betfair.event import get_events, lock_events
from apps.betfair.odd import get_odds, decide_winners, calculate_score
from apps.betfair.livescore import get_livescores
from apps.betfair.competition import get_competition_kinds, get_competitions
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'fetches betfair data'

    def handle(self, *args, **kwargs):
        get_competition_kinds()
        get_competitions()
        get_events()
        get_odds()
        #move that away
        lock_events()
        decide_winners()
        calculate_score()
        get_livescores()