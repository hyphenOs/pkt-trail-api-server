from django.urls import path
from pkt_trail_fe.apps.users import views

urlpatterns = [
    path("auth_github", views.auth_github, name="auth_github")
]