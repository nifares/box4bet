from django.contrib import admin
from apps.competition.models import CompetitionKind, Competition, Event, Odd

# Register your models here.

admin.site.register(CompetitionKind)
admin.site.register(Competition)
admin.site.register(Event)
admin.site.register(Odd)