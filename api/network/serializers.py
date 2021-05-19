from rest_framework import serializers, exceptions

from network.models import Connection, Follow

from userauth.serializers import UserSerializer, UserProfileSerializer


class ConnectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Connection
        fields  = ('date_time', 'has_been_accepted','is_visible','receiver','sender') 
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['connection_id'] = instance.id
        return response
        

class FollowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Follow
        fields  = '__all__'  
        
        
