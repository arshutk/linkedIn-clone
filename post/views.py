from django.shortcuts import render

from post.models import Post, Like, Celebrate, Support, Love, Insightful, Curious

from post.serializers import PostSerializer, LikeSerializer, CelebrateSerializer, SupportSerializer, LoveSerializer, \
                             InsightfulSerializer, CuriousSerializer

from rest_framework import views, generics

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import status

from rest_framework.response import Response

from django.http import Http404


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
        print(serializer.initial_data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save() 
            Vote.objects.create(post = self.get_post(serializer.data['id']))  
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# class VoteGetView(views.APIView):
    
#     def get_post(self, post_id):
#         try:
#             return Post.objects.get(id = post_id)
#         except:
#             raise Http404
        
    
#     def get(self, request, post_id):
#         post = self.get_post(post_id)
#         vote_list = list()
#         vote_list.append({'like': post.votes.like})
#         vote_list.append({'celebrate': post.votes.celebrate})
#         vote_list.append({'support': post.votes.support})
#         vote_list.append({'love': post.votes.love})
#         vote_list.append({'insightful': post.votes.insightful})
#         vote_list.append({'curious': post.votes.curious})
#         return Response({'votes': vote_list}, status=status.HTTP_200_OK)
    
    
# class VotePostView(views.APIView):

#     def get_post(self, post_id):
#         try:
#             return Post.objects.get(id = post_id)
#         except:
#             raise Http404
    
#     def get_vote_model(self, post_id):
#         try:
#             return Vote.objects.get(id = post_id)
#         except:
#             raise Http404

#     def post_upvote(self, user, post, vote_type):
#         setattr(post.votes, vote_type, getattr(post.votes, vote_type) + 1)
#         post.votes.upvoter.add(user)
#         post.votes.save()

#     def post_downvote(self, user, post, vote_type):
#         setattr(post.votes, vote_type, getattr(post.votes, vote_type) - 1)
#         post.votes.downvoter.add(user)
#         post.votes.save()
        

#     def post(self, request, post_id, vote_type):
        
#         post = self.get_post(post_id)
#         vote = int(request.data.get('vote'))
#         user = request.user.profile
        
#         if vote > 0:
#             if user in post.votes.upvoter.all():
#                 return Response({'detail': "Already upvoted"}, status=status.HTTP_400_BAD_REQUEST)
#             elif user in post.votes.downvoter.all():
#                 self.post_upvote(user, post, vote_type)
#                 post.votes.downvoter.remove(user)
#                 return Response({'detail':'Post has been upvoted'}, status=status.HTTP_200_OK)
#             self.post_upvote(user, post, vote_type)
#             return Response({'detail':'Post has been upvoted'}, status=status.HTTP_200_OK)
#         if user in post.votes.downvoter.all():
#                 return Response({'detail': "Already downvoted"},status=status.HTTP_400_BAD_REQUEST)
#         elif user in post.votes.upvoter.all():
#             self.post_downvote(user, post, vote_type)
#             post.votes.upvoter.remove(user)
#             return Response({'detail':'Post has been downvoted'},status=status.HTTP_200_OK)
#         self.post_downvote(user, post, vote_type)
#         return Response({'detail':'Post has been downvoted'},status=status.HTTP_200_OK)
