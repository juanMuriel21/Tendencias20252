from rest_framework import serializers


class UserRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()