"""
Module for our 'celery' App.
"""

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pkttrail.api.settings')

celery_app = Celery('pkttrail.api', include=['pkttrail.api.apps.resources.tasks'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.conf.beat_schedule = {
    'monitor_agents': {
        'task': 'pkttrail.api.apps.resources.tasks.monitor_agents',
        'schedule': 10,
        'args': ()
    }
}

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()


@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

