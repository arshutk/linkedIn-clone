from django.shortcuts import render

from post.models import Post, Vote, Comment, Reply

from post.serializers import PostSerializer, VoteSerializer, CommentSerializer, ReplySerializer

from rest_framework import views, generics

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import status

from rest_framework.response import Response

from django.http import Http404

from userauth.models import UserProfile

from datetime import datetime, timedelta, timezone

from django.shortcuts import get_object_or_404


class PostView(views.APIView):
    serializer_class = PostSerializer    
        
    def post(self, request):
        data = request.data.copy()
        # remove later
        media_type         = request.data.get('media_type')
        if media_type:
            if media_type == 'img':
                print(1)
                data['image_linked'] = data['media']
                serializer = PostSerializer(data = data, context = {'request': request})
                if serializer.is_valid():
                    serializer.save()  
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            data['video_linked'] = data['media']
            serializer = PostSerializer(data = data, context = {'request': request})
            if serializer.is_valid():
                serializer.save()  
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        # here
        serializer = PostSerializer(data = data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()  
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
                    return Response({'detail': "Already voted"}, status=status.HTTP_400_BAD_REQUEST)
                post.votes.filter(voter = user).delete()
                return Response({'detail': "Vote Removed"}, status = status.HTTP_200_OK)
        
        else: 
            if int(choice) > 0:
                data = dict()
                data.update({'post':post_id, 'vote_type': vote_type, 'voter':user.id})
                serializer = VoteSerializer(data = data, context = {'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response({'detail':'Voted'},status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'Post must be upvoted first.'},status=status.HTTP_404_NOT_FOUND)


class BookmarkView(views.APIView):
    
    def get_post(self, post_id):
        try:
            return Post.objects.get(id = post_id)
        except:
            raise Http404
        
    def post(self, request, post_id):
        post = self.get_post(post_id)
        user  = request.user.profile
        if user not in post.bookmarked_by.all():
            post.bookmarked_by.add(user)
            return Response({'detail': "Bookmark added"},status = status.HTTP_201_CREATED) 
        return Response({'detail': "Post already bookmarked"},status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        post = self.get_post(post_id)
        user  = request.user.profile
        if user in post.bookmarked_by.all():
            post.bookmarked_by.remove(user)
            return Response({'detail': "Bookmark removed"},status = status.HTTP_201_CREATED) 
        return Response({'detail': "Post is not bookmarked"},status = status.HTTP_400_BAD_REQUEST)
    
    
class GetBookmarks(views.APIView):

    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(id = user_id)
        except:
            raise Http404

    def get(self, request, user_id):
        user = self.get_user(user_id)
        forum = PostSerializer(user.bookmarked_posts.all(), many = True, context = {'request':request})
        return Response(forum.data, status = status.HTTP_200_OK)
    

class CommentPostView(views.APIView):
    
    def post(self, request):
        
        serializer = CommentSerializer(data = request.data, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
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

        if vote:
            if vote > 0:
                if user in liked_by.all():
                    return Response({'detail': "Already liked"},status=status.HTTP_304_NOT_MODIFIED)
                liked_by.add(user)
                return Response({'detail':'Liked'},status=status.HTTP_200_OK)
            if user in liked_by.all():
                liked_by.remove(user)
                return Response({'detail': "Like removed"},status=status.HTTP_204_NO_CONTENT)
            return Response({'detail':'Like the comment first'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Sufficient data not provided'},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, comment_id):
        comment = Comment.objects.get(id = comment_id)
        serializer = CommentSerializer(comment, data = request.data, partial = True, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class ReplyPostView(views.APIView):
    
    def post(self, request):
        serializer = ReplySerializer(data = request.data, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
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

        liked_by = self.get_reply(reply_id).liked_by
        if vote:
            if vote > 0:
                if user in liked_by.all():
                    return Response({'detail': "Already liked"},status=status.HTTP_304_NOT_MODIFIED)
                liked_by.add(user)
                return Response({'detail':'Liked'},status=status.HTTP_200_OK)
            if user in liked_by.all():
                liked_by.remove(user)
                return Response({'detail': "Like removed"},status=status.HTTP_204_NO_CONTENT)
            return Response({'detail':'Like the comment first'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Sufficient data not provided'},status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, reply_id):
        reply = self.get_reply(reply_id)
        serializer = ReplySerializer(reply, data = request.data, partial = True, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    