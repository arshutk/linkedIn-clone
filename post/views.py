from django.shortcuts import render

from post.models import Post, Vote, Comment, Reply, Hashtag

from post.serializers import PostSerializer, VoteSerializer, CommentSerializer, ReplySerializer, \
                             PostCreateSerializer, VoteCreateSerializer, CommentCreateSerializer, ReplyCreateSerializer

from rest_framework import views, generics

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import status

from rest_framework.response import Response

from django.http import Http404

from userauth.models import User, UserProfile

from network.models import Follow

from datetime import datetime, timedelta, timezone

from django.shortcuts import get_object_or_404

from rest_framework import filters

from notification.models import Notification

import re

from django.utils import timezone

from django.db.models import Count    

from django.http import JsonResponse

class PostView(views.APIView):
    serializer_class = PostCreateSerializer    
        
    def post(self, request):
        data = request.data.copy()
        # remove later
        media_type         = request.data.get('media_type')
        if media_type:
            if media_type == 'img':
                data['image_linked'] = data['media']
                serializer = PostCreateSerializer(data = data, context = {'request': request})
                if serializer.is_valid():
                    serializer.save()
                    topics = set(re.findall(r'\B#\w*[a-zA-Z]+\w*', data['text']))
                    for topic in topics:
                        Hashtag.objects.create(topic = topic)   
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            elif media_type == 'video':
                data['video_linked'] = data['media']
                serializer = PostCreateSerializer(data = data, context = {'request': request})
                if serializer.is_valid():
                    serializer.save() 
                    topics = set(re.findall(r'\B#\w*[a-zA-Z]+\w*', data['text']))
                    for topic in topics:
                        Hashtag.objects.create(topic = topic) 
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        # here
        serializer = PostCreateSerializer(data = data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            topics = set(re.findall(r'\B#\w*[a-zA-Z]+\w*', data['text']))
            for topic in topics:
                Hashtag.objects.create(topic = topic)   
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class GetPostView(views.APIView):
    def get(self, request, profile_id):
        user = get_object_or_404(UserProfile, id = profile_id)
        query = Post.objects.filter(written_by = user)
        serializer = PostSerializer(query, many = True, context = {'request': request, 'user': request.user})
        return Response(serializer.data, status = status.HTTP_200_OK)   

    
class VoteGetView(views.APIView):
    
    def get_post(self, post_id):
        try:
            return Post.objects.get(id = post_id)
        except:
            raise Http404    
    
    def get(self, request, post_id):
        post = self.get_post(post_id)
        vote_list = dict()
        vote_list.update({'like': post.votes.filter(vote_type = 'like').count()})
        vote_list.update({'celebrate': post.votes.filter(vote_type = 'celebrate').count()})
        vote_list.update({'support': post.votes.filter(vote_type = 'support').count()})
        vote_list.update({'love': post.votes.filter(vote_type = 'love').count()})
        vote_list.update({'insightful': post.votes.filter(vote_type = 'insightful').count()})
        vote_list.update({'curious': post.votes.filter(vote_type = 'curious').count()})        
        return Response(vote_list, status=status.HTTP_200_OK)
    
    
class VotePostView(views.APIView):
    def post(self, request, post_id, vote_type):
        post = get_object_or_404(Post, id = post_id)
        choice  = request.data.get('vote')
        user    = request.user.profile 
        votes   = post.votes.filter(voter = user)
        
        for vote in votes:
            if user == vote.voter:
                if int(choice) > 0:
                    return Response({'detail': "Already voted"}, status=status.HTTP_226_IM_USED)
                post.votes.filter(voter = user).delete()
                try:
                    Notification.objects.get(target = post.written_by, source = user,
                                             action = 'post_liked', action_id = post_id).delete()
                except:
                    pass
                return Response({'detail': "Vote Removed"}, status = status.HTTP_202_ACCEPTED)
        
        if int(choice) > 0:
            data = dict()
            data.update({'post':post_id, 'vote_type': vote_type, 'voter':user.id})
            serializer = VoteCreateSerializer(data = data, context = {'request': request})
            if serializer.is_valid():
                serializer.save()
                target = post.written_by
                if target != user:
                    Notification.objects.create(target = target, source = user, action = 'post_liked', 
                                                detail = 'liked your post.', action_id = post_id)
                return Response({'detail':'Voted'},status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Post must be upvoted first.'},status=status.HTTP_400_BAD_REQUEST)


class BookmarkView(views.APIView):       
    def post(self, request, post_id):
        print(request.data)
        post = get_object_or_404(Post, id = post_id)
        user  = request.user.profile
        if user not in post.bookmarked_by.all():
            post.bookmarked_by.add(user)
            return Response({'detail': "Bookmark added"},status = status.HTTP_201_CREATED) 
        return Response({'detail': "Post already bookmarked"},status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id = post_id)
        user  = request.user.profile
        if user in post.bookmarked_by.all():
            post.bookmarked_by.remove(user)
            return Response({'detail': "Bookmark removed"},status = status.HTTP_204_NO_CONTENT) 
        return Response({'detail': "Post is not bookmarked"},status = status.HTTP_400_BAD_REQUEST)
    
    
class GetBookmarks(views.APIView):
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id = user_id)
        forum = PostSerializer(user.bookmarked_posts.all(), many = True, context = {'request':request, 'user': user.user})
        return Response(forum.data, status = status.HTTP_200_OK)
    

class CommentPostView(views.APIView):
    def post(self, request):
        serializer = CommentCreateSerializer(data = request.data, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            target = Post.objects.get(id = serializer.data['post']).written_by 
            source = UserProfile.objects.get(id = serializer.data['commented_by'])
            if target != source:
                Notification.objects.create(target = target, source = source, action = 'commented',
                                            detail = 'commented on your post.', action_id = serializer.data['id'])
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class CommentUpdateView(views.APIView):
    def get_comment(self, comment_id):
        try:
            return Comment.objects.get(id = comment_id)
        except:
            raise Http404
    
    def post(self, request, comment_id):
        vote  = request.data.get('vote') 
        user  = request.user.profile
        
        liked_by = self.get_comment(comment_id).liked_by
        
        target = self.get_comment(comment_id).commented_by
        
        if vote:
            if vote > 0:
                if user in liked_by.all():
                    return Response({'detail': "Already liked"},status=status.HTTP_304_NOT_MODIFIED)
                liked_by.add(user)
                if target != user:
                    Notification.objects.create(target = target, source = user, action = 'comment_liked',
                                                detail = 'liked your comment.', action_id = comment_id)
                return Response({'detail':'Liked'},status=status.HTTP_200_OK)
            elif user in liked_by.all():
                liked_by.remove(user)
                if target != user:
                    Notification.objects.get(target = target, source = user, action = 'comment_liked', 
                                             action_id = comment_id).delete()
                return Response({'detail': "Like removed"},status=status.HTTP_204_NO_CONTENT)
            return Response({'detail':'Like the comment first'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Sufficient data not provided'},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, comment_id):
        comment = Comment.objects.get(id = comment_id)
        serializer = CommentCreateSerializer(comment, data = request.data, partial = True, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class ReplyPostView(views.APIView):
    def post(self, request):
        serializer = ReplyCreateSerializer(data = request.data, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            target = Comment.objects.get(id = serializer.data['comment']).commented_by 
            source = UserProfile.objects.get(id = serializer.data['replied_by'])
            if target != source:
                Notification.objects.create(target = target, source = source, action = 'commented', 
                                            detail = 'replied to your comment.', action_id = serializer.data['id'])
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
       
class ReplyUpdateView(views.APIView):
    def get_reply(self, reply_id):
        try:
            return Reply.objects.get(id = reply_id)
        except:
            raise Http404
    
    def post(self, request, reply_id):
        vote  = request.data.get('vote') 
        user  = request.user.profile

        target = self.get_reply(reply_id).replied_by
        
        liked_by = self.get_reply(reply_id).liked_by
        if vote:
            if int(vote) > 0:
                if user in liked_by.all():
                    return Response({'detail': "Already liked"},status=status.HTTP_304_NOT_MODIFIED)
                liked_by.add(user)
                if user != target:
                    Notification.objects.create(target = target, source = user, action = 'reply_liked', 
                                                detail = 'liked your reply.', action_id = reply_id)
                return Response({'detail':'Liked'},status=status.HTTP_200_OK)
            if user in liked_by.all():
                liked_by.remove(user)
                if user != target:
                    Notification.objects.get(target = target, source = user, action = 'reply_liked',
                                             action_id = reply_id).delete()
                return Response({'detail': "Like removed"},status=status.HTTP_204_NO_CONTENT)
            return Response({'detail':'Like the comment first'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Sufficient data not provided'},status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, reply_id):
        reply = self.get_reply(reply_id)
        serializer = ReplyCreateSerializer(reply, data = request.data, partial = True, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class HashtagView(views.APIView):
    def get(self, request):
        query = Hashtag.objects.filter(time__gte = timezone.localtime(timezone.now()) - timezone.timedelta(days = 5)).\
                values('topic').annotate(Count('topic')).order_by('-topic__count')
        return JsonResponse(list(query), safe=False)
        
        


class FeedView(views.APIView):
    def get_commented_post(self, following):
        query = list()
        for person in following: 
            for comment in person.comments_made.all():
                query.append(comment.post)
        return query
    
    def get_liked_post(self, following):
        query = list()
        for person in following:
            for vote in person.votes.filter(vote_type = 'like').all():
                query.append(vote.post)
        return query
                
    def get(self, request):  
        user = request.user.profile
        user_following = Follow.objects.filter(follower = user).all()
        # user_posts = Post.objects.filter(written_by = user).all()
        response = list()
        for person in user_following:
            for vote in person.user.votes.filter(vote_type = 'like').all(): 
                if vote.post in response:
                    continue
                serializer = PostSerializer(vote.post, context = {'request':request, 'user':user.user})
                data = serializer.data.copy()
                data['message'] = f'{person.user.first_name} {person.user.last_name} liked this post'
                response.append(data)
            for comment in person.user.comments_made.all():
                if comment.post in response:
                    continue
                serializer = PostSerializer(comment.post, context = {'request':request, 'user':user.user})
                data = serializer.data.copy()
                data['message'] = f'{person.user.first_name} {person.user.last_name} commented on this post'
                response.append(data)
        for user_followed in user_following:
            posts = Post.objects.filter(written_by = user_followed.user).all()
            for post in posts:
                if post in response:
                    continue
                serializer = PostSerializer(post, context = {'request':request, 'user':user.user})
                data = serializer.data.copy()
                data['message'] = None
                response.append(data)
        return Response(response, status = status.HTTP_200_OK)
            
        # for post in user_posts:
        #     if post in response:
        #             continue
        #     serializer = PostSerializer(post, context = {'request': request, 'user': user.user})
        #     data = serializer.data.copy()
        #     data['message'] = None
        #     response.append(data)
        # return Response(response, status = status.HTTP_200_OK)
        
        
         
# Search
class PostSearchView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', ]
    
    def get_serializer_context(self):
        # print(self.request.query_params.get('radius'))
        context = super(PostSearchView, self).get_serializer_context()
        context.update({"request": self.request, 'user': self.request.user})
        return context


    