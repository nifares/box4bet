from django.urls import path
from .views import home, events

urlpatterns = [
    path('', home),
    path('events', events)
]
