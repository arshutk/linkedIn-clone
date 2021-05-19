from django.shortcuts import render

from rest_framework import viewsets

from django.shortcuts import render

from rest_framework import status

from rest_framework.response import Response

from chat.models import Chat, Thread

from userauth.models import UserProfile

from userauth.serializers import UserProfileSerializer

from django.http import Http404

from django.shortcuts import get_object_or_404

from chat.serializers import ChatSerializer, ThreadSerializer, ChatListSerializer

from rest_framework import views

class GetChatList(views.APIView):
    
    def get(self, request):
        user = request.user.profile
        threads = Thread.objects.filter(first_member = user) | Thread.objects.filter(second_member = user)
        serializer = ChatListSerializer(threads, many = True, context = {'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)