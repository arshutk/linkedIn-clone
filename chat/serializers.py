from rest_framework import serializers

from chat.models import Thread, Chat

from userauth.serializers import UserProfileSerializer

               
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields =('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sender'] = instance.sender.first_name
        response['is_my_msg'] = True if instance.sender.id == self.context.get('sender') else False
        response['sender_id'] = instance.sender.id
        return response
    
    
class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields =('__all__')
        

class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields =('id',)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if not self.context.get('request').user.profile == instance.first_member:
            response['user_id'] = instance.first_member.id
            try:
                response['user_avatar'] = self.context['request'].build_absolute_uri(instance.first_member.avatar)
            except:
                response['user_avatar'] = None
            response['user_name'] = instance.first_member.first_name
            try:
                response['text'] = instance.messages.first().text
            except:
                response['text'] = None
        else:
            response['user_id'] = instance.second_member.id
            try:
                response['user_avatar'] = self.context['request'].build_absolute_uri(instance.second_member.avatar.url)
            except:
                response['user_avatar'] = None
            response['user_name'] = instance.second_member.first_name
            try:
                response['text'] = instance.messages.first().text
            except:
                response['text'] = None
        return response
    
