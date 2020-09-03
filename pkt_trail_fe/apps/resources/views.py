import os
import json

from rest_framework.viewsets import ModelViewSet

from .models import PktTrailResource
from .serializers import PktTrailResourceSerializer

class PktTrailResourceViewSet(ModelViewSet):

    queryset = PktTrailResource.objects.all()
    serializer_class = PktTrailResourceSerializer
