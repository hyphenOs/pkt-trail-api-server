from django.urls import path
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from .views import PktTrailResourceViewSet

router = DefaultRouter()
router.register(r'', PktTrailResourceViewSet)

urlpatterns = [
    path("", include(router.urls))
]
