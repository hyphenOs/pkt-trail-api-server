"""
Tasks related to interface with the agents running.
"""
import logging
from datetime import timedelta

from django.utils import timezone

from pkttrail.api.celery import celery_app

from .models import PktTrailResource

_RESOURCE_NO_KEEP_ALIVE_TIMEOUT = 30

_logger = logging.getLogger(__name__)

@celery_app.task()
def monitor_agents():

    print("Running Task..")
    keep_alive_timeout = timezone.now() + timedelta(
            seconds=-_RESOURCE_NO_KEEP_ALIVE_TIMEOUT)

    not_updated_online_resources = PktTrailResource.objects.filter(
            state=2,
            last_updated_at__lte=keep_alive_timeout)

    # Go ahead mark each of these resources as offline.
    for resource in not_updated_online_resources:
        _logger.warning("Resource: %s is Online, but Keep Alive Not Received.",
                resource.name)
        resource.state = 1
        resource.save()

    _logger.info("Marked %d resources as offline.",
            not_updated_online_resources.count())
