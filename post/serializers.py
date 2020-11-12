from rest_framework import serializers

from post.models import Post, Vote, Upvoter, Downvoter

from userauth.models import User, UserProfile

from userauth.serializers import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Post
        fields  = '__all__'
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['written_by'] = UserProfileSerializer(instance.written_by, context = {'request': self.context.get('request')}).data
        return response
    
    
class VoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Vote
        fields  = '__all__'
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['post'] = PostSerializer(instance.post, context = {'request': self.context.get('request')}).data
        return response
    
class UpvoterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Upvoter
        fields  = '__all__'
        
    
class DownvoterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Downvoter
        fields  = '__all__'
    
    
    