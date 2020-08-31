from django.urls import path
from pkt_trail_fe.apps.resources import views

urlpatterns = [
    path("", views.ResourceView.as_view(), name="resources"),
]
