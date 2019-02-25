from django.conf import settings
from rest_framework import serializers

from programs.models import Pr as Programs

class ProgramsSerializer(serializers.ModelSerializer):
    activeFrom = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    activeTo = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    class Meta:
        model = Programs
        fields = ('programId', 'name', 'description', 'photo', 'schedule', 'activeFrom', 'activeTo', 'channel', 'active', 'points')
