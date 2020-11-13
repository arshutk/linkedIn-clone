from rest_framework import serializers

from post.models import Post, Vote
# , Like, Celebrate, Support, Love, Insightful, Curious

from userauth.models import User, UserProfile

from userauth.serializers import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Post
        fields  = '__all__'
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['written_by'] = UserProfileSerializer(instance.written_by, context = {'request': self.context.get('request')}).data['id']
        return response
    
    
# class LikeSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model   = Like
#         fields  = '__all__'

# class CelebrateSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model   = Celebrate
#         fields  = '__all__'
        
        
# class SupportSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model   = Support
#         fields  = '__all__'
        
# class LoveSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model   = Love
#         fields  = '__all__'
        
# class InsightfulSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model   = Insightful
#         fields  = '__all__'
        
# class CuriousSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model   = Curious
#         fields  = '__all__'
        
class VoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Vote
        fields  = '__all__'
        
