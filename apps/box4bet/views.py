from django.shortcuts import render
from apps.box4bet.models import Event

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def events_view(request):
    data = {
        'events': Event.objects.order_by('start_time').all()
    }
    return render(request, 'events_view.html', data)

def event(request, event_id):
    data = {
        'event': Event.objects.get(pk=event_id)
    }
    return render(request, 'event.html', data)