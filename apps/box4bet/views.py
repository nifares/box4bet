import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from apps.box4bet.models import Event, Bet, Odd
from apps.box4bet.forms import CustomUserCreationForm

LOG = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, 'home.html', {} )

def events_view(request):
    data = {
        'events': Event.objects.order_by('start_time').all()
    }
    return render(request, 'events_view.html', data)

def event(request, event_id):
    data = {
        'event': Event.objects.get(pk=event_id),
    }
    if request.user.is_authenticated:
        data['user_bet'] = request.user.bet_set.filter(event=event_id).first()
    return render(request, 'event.html', data)

def register(request):
    form = CustomUserCreationForm
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): 
            print('valid')
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))
        else:
            form = form
    return render(
        request,
        "registration/register.html",
        {"form": form}
    )

def bet(request, event_id):
    if request.method == "POST" and request.user.is_authenticated:
        obj, created = Bet.objects.update_or_create(
            user = request.user,
            event = Event.objects.get(pk=event_id),
            defaults = {
                'odd': Odd.objects.get(pk=request.POST['odd'])
            }
        )
        action = 'created' if created else 'updated'
        LOG.info(
            '{} {} bet for event "{}" [{}] to {} [{}]'.format(
                obj.user.username,
                action,
                obj.event.name,
                obj.event.id,
                obj.odd.name,
                obj.odd.prize
            )
        )
        
    return redirect(f"/events/{event_id}")