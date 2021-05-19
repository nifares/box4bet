from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from apps.box4bet.models import Event
from apps.box4bet.forms import CustomUserCreationForm
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
        'event': Event.objects.get(pk=event_id)
    }
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