from rest_framework import serializers, exceptions

from network.models import Connection

from userauth.serializers import UserSerializer, UserProfileSerializer


class ConnectionSerializer(serializers.ModelSerializer):
    connection_id = serializers.CharField(source = 'id')
    
    class Meta:
        model   = Connection
        fields  = ('connection_id','date_time', 'has_been_accepted','is_visible','receiver','sender')  
        
        
