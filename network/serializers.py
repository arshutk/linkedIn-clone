from rest_framework import serializers, exceptions

from network.models import Connection

from userauth.serializers import UserSerializer, UserProfileSerializer


class ConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Connection
        fields  = '__all__'   
        
