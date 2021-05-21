from django.conf.urls import include
from django.urls import path
import apps.box4bet.views as views
urlpatterns = [
    path('', views.home, name="home"),
    path('events', views.events_view),
    path('events/<int:event_id>', views.event),
    path('events/<int:event_id>/bet', views.bet),
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', views.register, name="register")
]
