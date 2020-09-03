from rest_framework import serializers

from .models import PktTrailResource, PktTrailService

class PktTrailServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PktTrailService
        fields = '__all__'

class PktTrailResourceSerializer(serializers.ModelSerializer):

    services = PktTrailServiceSerializer(many=True, read_only=True)

    class Meta:
        model = PktTrailResource
        fields = '__all__'

