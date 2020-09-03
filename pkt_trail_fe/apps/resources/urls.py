from django.urls import path
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from pkt_trail_fe.apps.resources.views import PktTrailResourceViewSet

router = DefaultRouter()
router.register(r'', PktTrailResourceViewSet)

urlpatterns = [
    path("", include(router.urls))
]
