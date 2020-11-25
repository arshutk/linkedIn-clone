from rest_framework import serializers

from post.models import Post, Vote, Comment, Reply

from userauth.models import User, UserProfile

from userauth.serializers import UserProfileSerializer

from django.utils import timezone


class PostCreateSerializer(serializers.ModelSerializer):
     class Meta:
        model   = Post
        fields  = '__all__'
        
class CommentCreateSerializer(serializers.ModelSerializer):
     class Meta:
        model   = Comment
        fields  = '__all__'
        
class ReplyCreateSerializer(serializers.ModelSerializer):
     class Meta:
        model   = Reply
        fields  = '__all__'
        
class VoteCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Vote
        fields  = '__all__'



def get_avatar(instance, context, query):
        try:
            profile = getattr(instance, query)
            name = profile.avatar.url
            url  = context['request'].build_absolute_uri(name)
            return url
        except:
            return None

def get_posted_at(query):
        time = timezone.localtime(timezone.now()) - query
        if time.days < 7:
            if time.days == 0:
                created_at = 'today'
            elif time.days == 1:
                created_at = 'yesterday'
            else:
                created_at = f'{time.days} days'
        elif time.days < 30:
            if int(time.days/7) == 1:
                created_at = '1 week'
            else:
                created_at = f'{int(time.days/7)} weeks'
        elif time.days < 365:
            if int(time.days/30) == 1:
                created_at = '1 month'
            else:
                created_at = f'{int(time.days/30)} months'
        else:
            if int(time.days/365) == 1:
                created_at = '1 year'
            else:
                created_at = f'{int(time.days/365)} years'
        return created_at  
    
    
class PostSerializer(serializers.ModelSerializer):
    is_liked_by_user = serializers.SerializerMethodField('get_is_liked')
    is_saved_by_user = serializers.SerializerMethodField('get_is_saved')

    class Meta:
        model   = Post
        fields  = ('id', 'text', 'posted_at', 'media_type', 'is_liked_by_user', 'is_saved_by_user')
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['posted_at'] = get_posted_at(instance.posted_at)
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
            comment_data = CommentSerializer(comment, context={'request': self.context.get('request'), 
                                                               'user': self.context.get('user')}).data
            replies_data = ReplySerializer(comment.replies.all(), many = True, context={'request': self.context.get('request'), 
                                                                'user': self.context.get('user')}).data
            query.append({'comment':comment_data, 'replies':replies_data})
        return query
        
    def get_is_liked(self, instance):
        if instance.votes.filter(vote_type = 'like', voter = self.context['user'].profile):
            return True
        return False
        
    def get_is_saved(self, instance):
        if self.context['user'].profile in instance.bookmarked_by.all():
            return True
        return False
    
    
        
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
    is_liked_by_user = serializers.SerializerMethodField('get_is_liked')
    
    class Meta:
        model   = Comment
        fields = ('id','text','posted_at', 'post', 'commented_by', 'liked_by', 'is_liked_by_user', )
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['posted_at'] = get_posted_at(instance.posted_at)
        response['likes_count']= instance.liked_by.count()
        response['author_id']= instance.commented_by.id
        response['author_name'] = f'{instance.commented_by.first_name} {instance.commented_by.last_name}'
        response['author_avatar'] = get_avatar(instance, self.context, 'commented_by')
        response['author_tagline'] = instance.commented_by.social_profile.tagline
        return response
    
        
    def get_is_liked(self, instance):
        if self.context['user'].profile in instance.liked_by.all():
            return True
        return False
        
        
class ReplySerializer(serializers.ModelSerializer):
    is_liked_by_user = serializers.SerializerMethodField('get_is_liked')
    
    class Meta:
        model   = Reply
        fields = ('id','text','posted_at', 'comment', 'replied_by', 'liked_by', 'is_liked_by_user', )
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['posted_at'] = get_posted_at(instance.posted_at)
        response['likes_count']= instance.liked_by.count()
        response['author_id']= instance.replied_by.id
        response['author_name'] = f'{instance.replied_by.first_name} {instance.replied_by.last_name}'
        response['author_avatar'] = get_avatar(instance, self.context, 'replied_by')
        response['author_tagline'] =  instance.replied_by.social_profile.tagline
        return response
    
    def get_is_liked(self, instance):
        if self.context['user'].profile in instance.liked_by.all():
            return True
        return False
        
# class TrendingSerializer(serializers.ModelSerializer):
#     topic = TrendingSerializer(many = True)
    
#     class Meta:
#         model = Trending
#         fields = ('topic', 'time')
        
#     def create(self, validated_data):
#         tracks_data = validated_data.pop('tracks')
#         topic = Trending.objects.create(**validated_data)
#         for track_data in tracks_data:
#             Track.objects.create(album=album, **track_data)
#         return album
