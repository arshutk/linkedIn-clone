from rest_framework import serializers, exceptions

from network.models import Connection

from userauth.serializers import UserSerializer, UserProfileSerializer


class ConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Connection
        fields  = '__all__'   
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['sender']   = UserProfileSerializer(instance.sender, context = {'request': self.context.get('request')}).data
        response['receiver'] = UserProfileSerializer(instance.receiver, context = {'request': self.context.get('request')}).data
        return response

