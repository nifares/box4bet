from django.contrib import admin
from apps.competition.models import CompetitionKind, Competition, Event, Odd, BetfairSession

# Register your models here.

admin.site.register(CompetitionKind)
admin.site.register(Competition)
admin.site.register(Event)
admin.site.register(Odd)
admin.site.register(BetfairSession)