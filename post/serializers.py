from rest_framework import serializers

from post.models import Post, Vote, Comment, Reply

from userauth.models import User, UserProfile

from userauth.serializers import UserProfileSerializer

def get_avatar(instance, context, query):
        try:
            profile = getattr(instance, query)
            name = profile.avatar.url
            url  = context['request'].build_absolute_uri(name)
            return url
        except:
            return None
        
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Post
        fields  = ('id', 'text', 'posted_at', 'media_type', )
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['media'] = self.get_post_media(instance)
        response['viewer_name'] = f'{self.context["user"].profile.first_name} {self.context["user"].profile.last_name}'
        response['viewer_avatar'] = get_avatar(self.context['user'], self.context, 'profile')
        response['viewer_tagline'] = self.context['user'].profile.social_profile.tagline
        response['author_id'] = instance.written_by.id
        response['author_name'] = f'{instance.written_by.first_name} {instance.written_by.last_name}'
        response['author_avatar'] = get_avatar(instance, self.context, 'written_by')
        response['author_tagline'] =  instance.written_by.social_profile.tagline
        response['likes_count'] =  instance.votes.filter(vote_type = 'like').count()
        response['comment_count'] =  instance.comments.count()
        response['liked_by'] =  self.get_liked_by(instance)
        response['comments'] =  self.get_comments(instance)
        return response

    def get_post_media(self, instance):
        media_type = instance.media_type
        if media_type == 'img':
            try:
                url  = self.context['request'].build_absolute_uri(instance.image_linked.url)
                return url
            except:
                return None
        try:
            url  = self.context['request'].build_absolute_uri(instance.video_linked.url)
            return url
        except:
            return None   
        
    def get_liked_by(self, instance):
        liked_by = instance.votes.filter(vote_type = 'like').all()
        serializer = VoteSerializer(liked_by, many = True, context={'request': self.context.get('request')})
        return serializer.data
    
    def get_comments(self, instance):
        comments = instance.comments.all()
        query = list()
        for comment in comments:
            comment_data = CommentSerializer(comment, context={'request': self.context.get('request')}).data
            replies_data = ReplySerializer(comment.replies.all(), many = True, context={'request': self.context.get('request')}).data
            query.append({'comment':comment_data, 'replies':replies_data})
        return query
        
        
class VoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Vote
        fields  = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['voter_name']= f'{instance.voter.first_name} {instance.voter.last_name}'
        response['voter_avatar'] = get_avatar(instance, self.context, 'voter')
        response['voter_tagline'] = instance.voter.social_profile.tagline
        return response
        
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Comment
        fields = '__all__'
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['likes_count']= instance.liked_by.count()
        response['author_id']= instance.commented_by.id
        response['author_name'] = f'{instance.commented_by.first_name} {instance.commented_by.last_name}'
        response['author_avatar'] = get_avatar(instance, self.context, 'commented_by')
        response['author_tagline'] = instance.commented_by.social_profile.tagline
        return response
        
class ReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Reply
        fields  = '__all__'
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['likes_count']= instance.liked_by.count()
        response['author_id']= instance.replied_by.id
        response['author_name'] = f'{instance.replied_by.first_name} {instance.replied_by.last_name}'
        response['author_avatar'] = get_avatar(instance, self.context, 'replied_by')
        response['author_tagline'] =  instance.replied_by.social_profile.tagline
        return response
        
