import uuid

from django.db import models

# Create your models here.

class PktTrailResource(models.Model):
    """ A class representing a 'resource' in Packet Trail.

    A resource is either a VM, or a Host or a k8s Cluster. Each of the
    resources can be managed through access_url.
    """

    RESOURCE_STATES = [
            (0, "Provisioned"),
            (1, "Offline"),
            (2, "Online"),
            (3, "Capture Active"),
            (4, "Error")
        ]

    RESOURCE_TYPES = [
            (0, "VM/Os"),
            (1, "k8s")
        ]

    name = models.CharField(max_length=100, blank=False, null=False)
    state = models.IntegerField(null=False, default=0, choices=RESOURCE_STATES)
    res_type = models.IntegerField(null=False, default=0, choices=RESOURCE_TYPES)
    owner = models.ForeignKey('users.PktTrailUser', related_name='resources', on_delete=models.CASCADE)
    agent_url = models.URLField()
    data_url = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    details = models.CharField(max_length=512, blank=True, null=True)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)

    class Meta:
        ordering = ('-created_at',)
        db_table = 'pkt_trail_resources'

class PktTrailService(models.Model):
    """ A Class representing a 'service' in Packet Trail.

    Packets can be captured at the granularity of a Service in Packet Trail.
    That is while starting a packet capture on a resource, the service
    identifies the filter that is to be applied."""

    SERVICE_STATES = [
            (-1, "Unknown"),
            (0, "Running"),
            (1, "Stopped"),
            (2, "Error")
        ]

    name = models.CharField(max_length=100, blank=True, null=False)
    proto = models.CharField(max_length=8, blank=True, null=False)
    interface = models.CharField(max_length=16, blank=True, null=False)
    port = models.IntegerField()
    filter_str = models.CharField(max_length=64, blank=True, null=False)
    resource = models.ForeignKey('resources.PktTrailResource', related_name='services', on_delete=models.CASCADE)
    details = models.CharField(max_length=100, blank=True, null=True)
    state = models.IntegerField(null=False, default=-1, choices=SERVICE_STATES)

    class Meta:
        db_table = 'pkt_trail_services'
