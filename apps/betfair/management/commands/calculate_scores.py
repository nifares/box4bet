from django.core.management.base import BaseCommand
from apps.betfair.odd import decide_winners, calculate_score

class Command(BaseCommand):
    help = 'decide on winning odds and calculate user score'
    def handle(self, *args, **kwargs):
        decide_winners()
        calculate_score()