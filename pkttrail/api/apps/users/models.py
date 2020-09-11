from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class PktTrailUser(AbstractUser):

    AUTH_PROVIDERS = [
            ('Github', 'Github')
        ]

    provider_id = models.CharField(max_length=32, null=False, blank=False)
    auth_provider = models.CharField(max_length=32,
            choices=AUTH_PROVIDERS,
            default='Github')
    profile_url = models.CharField(max_length=100, null=True, blank=True)
    avatar_url = models.CharField(max_length=100, null=True, blank=False)
