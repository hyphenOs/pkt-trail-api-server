from django.urls import path
from pkt_trail_fe.apps.users import views

urlpatterns = [
    path("authenticate", views.authenticate, name="authenticate")
]