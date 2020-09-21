from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework import status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response


from pkttrail.schema.messages import (
        PktTrailSchemaValidationError,
        PktTrailInitRequestSchema,
        PktTrailKeepAliveRequestSchema
    )


class PktTrailAgentsViewSet(viewsets.ViewSet):


    @action(detail=False, methods=['post'])
    def init(self, request):
        """Handler for `init` request from the agent."""

        try:
            init_req = PktTrailInitRequestSchema().loads(
                    request.body.decode("utf-8"))

            return Response(dict(message="ok"))

        except PktTrailSchemaValidationError:
            return Response(dict(message="Bad Request"),
                    status=http_status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def keepalive(self, request):
        """Handler for `keep-alive` request from the agent."""
        try:
            keep_alive_req = PktTrailKeepAliveRequestSchema().loads(
                    request.body.decode("utf-8"))

            return Response(dict(message="ok"))

        except PktTrailSchemaValidationError:
            return Response(dict(message="Bad Request"),
                    status=http_status.HTTP_400_BAD_REQUEST)
