from django.shortcuts import render

from post.models import Post, Vote

from post.serializers import PostSerializer, VoteSerializer

from rest_framework import views, generics

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import status

from rest_framework.response import Response

from django.http import Http404

from userauth.models import UserProfile


class PostView(generics.ListCreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_post(self, post_id):
        try:
            return Post.objects.get(id = post_id)
        except:
            raise Http404
        
    def post(self, request):
        data = request.data
        data['written_by'] = request.user.profile.id
        serializer = PostSerializer(data = data, context = {'request': request})
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()  
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


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

    def get_post(self, post_id):
        try:
            return Post.objects.get(id = post_id)
        except:
            raise Http404

    def post_upvote(self, user, post, vote_type):
        query = getattr(post,vote_type)
        query.vote += 1
        query.upvoter.add(user)
        query.save()

    def post_downvote(self, user, post, vote_type):
        query = getattr(post,vote_type)
        query.vote -= 1
        query.downvoter.add(user)
        query.save()
        

    def post(self, request, post_id, vote_type):
        
        post    = self.get_post(post_id)
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
            return Response({'msg': "Bookmark added"},status = status.HTTP_201_CREATED) 
        return Response({'msg': "Post already bookmarked"},status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        post = self.get_post(post_id)
        user  = request.user.profile
        if user in post.bookmarked_by.all():
            post.bookmarked_by.remove(user)
            return Response({'msg': "Bookmark removed"},status = status.HTTP_201_CREATED) 
        return Response({'msg': "Post is not bookmarked"},status = status.HTTP_400_BAD_REQUEST)
    
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
    
        
            
            
