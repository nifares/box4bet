from django.core.management.base import BaseCommand
from apps.betfair.livescore import get_livescores

class Command(BaseCommand):
    help = 'get livescores'
    def handle(self, *args, **kwargs):
        get_livescores()