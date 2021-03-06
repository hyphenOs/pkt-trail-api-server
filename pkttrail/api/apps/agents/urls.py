from django.urls import path
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from .views import PktTrailAgentsViewSet

router = DefaultRouter()
router.register(r'', PktTrailAgentsViewSet, basename="agents.urls")

urlpatterns = [
    path("", include(router.urls))
]
