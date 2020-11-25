from rest_framework import serializers

from chat.models import Thread, Chat

from userauth.serializers import UserProfileSerializer

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields =('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sender']     = UserProfileSerializer(instance.sender, context = {'request': self.context.get('request')}).data
        return response
    
class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields =('__all__')
    
