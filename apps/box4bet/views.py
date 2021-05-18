from django.shortcuts import render
from apps.box4bet.models import Event

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def events(request):
    data = {
        'events': Event.objects.all()
    }
    return render(request, 'events.html', data)