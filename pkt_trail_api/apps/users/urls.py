from django.urls import path

from . import views

urlpatterns = [
    path("auth_github", views.auth_github, name="auth_github")
]
