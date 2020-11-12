from django.shortcuts import render

from post.models import  Post, Vote

from post.serializers import PostSerializer, VoteSerializer

from rest_framework import views

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import status

from rest_framework.response import Response

from django.http import Http404


class PosttView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Document.objects.all()
        category = self.request.GET.get('category','')
        college  = self.request.GET.get('college','')
        stars    = self.request.GET.get('stars','')

        if category:
            if college is None and stars is None:
                queryset = queryset.filter(category__icontains = category)
            elif college:
                queryset = queryset.filter(category__icontains = category, college = college)
            else:
                queryset = queryset.filter(category__icontains = category, stars = stars)
            return queryset
        elif college: 
            if stars:
                queryset = queryset.filter(college = college, stars = stars)
            queryset = queryset.filter(college = college)
            return queryset
        else:
            queryset = queryset.filter(stars = stars)
        return queryset
    
    def post(self, request):
        data = request.data
        data['uploader'] = request.user.profile.id
        serializer = DocumentSerializer(data = data, context = {'request': request})
        print(serializer.initial_data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()   
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_201_CREATED)
