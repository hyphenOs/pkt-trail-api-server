import logging

from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework import status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response

from pkttrail.schema.messages import (
        OS_AGENT_INIT_MESSAGE,
        OS_AGENT_KEEPALIVE_MESSAGE,
    )

from pkttrail.schema.messages import (
        PktTrailSchemaValidationError,
        PktTrailInitRequestSchema,
        PktTrailKeepAliveRequestSchema
    )


from ..resources.models import (
        PktTrailResource,
        PktTrailService
    )

from .messages import (
        get_api_response_ok
    )

_logger = logging.getLogger(__name__)

class PktTrailAgentsViewSet(viewsets.ViewSet):


    def _get_resource_from_request(self, request):

        agent_uuid = request['params']['agentUUID']

        try:
            resource = PktTrailResource.objects.get(uuid=str(agent_uuid))
            return resource
        except PktTrailResource.NotFound:
            _logger.warning("Resource Not found for UUID: %s, Method: %s, Id: %s",
                    agent_uuid, request['method'], request['id'])

            return None


    @action(detail=False, methods=['post'])
    def init(self, request):
        """Handler for `init` request from the agent."""

        try:
            init_req = PktTrailInitRequestSchema().loads(request.body.decode("utf-8"))

            resource = self._get_resource_from_request(init_req)
            if resource is None:
                return Response(dict(message="Not Found."),
                        status=http_status.HTTP_404_NOT_FOUND)

            _logger.debug("Init Request: %s", init_req)

            msgid = init_req["id"]
            response = get_api_response_ok(OS_AGENT_INIT_MESSAGE, msgid)
            print(response)
            return Response(response)

        except PktTrailSchemaValidationError:
            return Response(dict(message="Bad Request"),
                    status=http_status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def keepalive(self, request):
        """Handler for `keep-alive` request from the agent."""
        try:
            keepalive_req = PktTrailKeepAliveRequestSchema().loads(
                    request.body.decode("utf-8"))

            _logger.debug("KeepAlive Request: %s", keepalive_req)

            # 1. Get the Resource or else return 404
            resource = self._get_resource_from_request(keepalive_req)
            if resource is None:
                return Response(dict(message="Not Found."),
                        status=http_status.HTTP_404_NOT_FOUND)

            # 2. Update all Services.
            services = keepalive_req['params']['services']
            ports = [s['port'] for s in services]
            agent_uuid = str(keepalive_req['params']['agentUUID'])

            for service in resource.services.all():
                try:
                    ports.remove(service.port)
                    service.state = 0
                    service.save()
                except ValueError:
                    # Service port exists, but not in the current list,
                    # mark this as inactive.
                    service.state = 1
                    service.save()

            # Whatever 'ports' remain now, there does not exist service for them.
            # Go ahead and create it and set state as started.
            for port in ports:
                for service in services:
                    if service['port'] == port:
                        service['resource'] = resource
                        service['state'] = 0
                        service_obj = PktTrailService.objects.create(**service)

            # 3. All is Well - Return success
            msgid = keepalive_req["id"]
            response = get_api_response_ok(OS_AGENT_KEEPALIVE_MESSAGE, msgid)
            return Response(response)

        except PktTrailSchemaValidationError:
            return Response(dict(message="Bad Request"),
                    status=http_status.HTTP_400_BAD_REQUEST)
