from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from pkttrail.schema.messages import PktTrailInitRequestSchema


class PktTrailAgentsViewSet(viewsets.ViewSet):


    @action(detail=False, methods=['post'])
    def init(self, request):
        return Response(dict(message="ok"))


    @action(detail=False, methods=['post'])
    def keepalive(self, request):
        return Response(dict(message="ok"))
