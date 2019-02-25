
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, is_password_usable
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import UserLog

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    points = serializers.CharField(read_only=True)
    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name", 'city', 'phone', "points", "address" )
        skip_update_fields = ("email",)

    def update(self, instance, validated_data):
        for skipField in self.Meta.skip_update_fields:
            if skipField in validated_data:
                validated_data.pop(skipField)
        return super(UserProfileSerializer, self).update(instance, validated_data)

class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = ( "eventType", 'details', 'points', "time" )
