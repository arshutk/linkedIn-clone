from django.shortcuts import render

from rest_framework import views, generics

from userauth.serializers import UserSerializer, UserProfileSerializer, UserExperienceSerializer

from userauth.models import User, UserProfile, UserExperience

from rest_framework.response import Response

from django.http import Http404

from rest_framework import status

from rest_framework.permissions import AllowAny

class UserCreateView(views.APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_201_CREATED)

class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class  = UserSerializer
    
    
    
        
        
