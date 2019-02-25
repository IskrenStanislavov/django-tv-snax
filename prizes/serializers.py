from django.conf import settings
from rest_framework import serializers

from prizes.models import Kind

class PrizesSerializer(serializers.ModelSerializer):
    activeFrom = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    activeTo = serializers.DateTimeField(format=settings.DATETIME_FORMAT)

    bought = serializers.SerializerMethodField()
    def get_bought(self, obj):
    	return obj.boughtByUser(self.currentUser)

    def __init__(self, user, *a, **ka):
    	self.currentUser = user
    	super(PrizesSerializer, self).__init__(*a, **ka)

    class Meta:
        model = Kind
        fields = ('prizeId', 'name', 'points', 'description', 'photo', 'activeFrom', 'activeTo', 'active', "bought")

