from django.urls import path
import apps.box4bet.views as views
urlpatterns = [
    path('', views.home),
    path('events', views.events_view),
    path('events/<int:event_id>', views.event)
]
