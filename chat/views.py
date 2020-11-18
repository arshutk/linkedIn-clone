from django.shortcuts import render

from rest_framework import viewsets

from django.shortcuts import render

from rest_framework import status

from rest_framework.response import Response

from chat.models import Chat

from userauth.models import UserProfile

from userauth.serializers import UserProfileSerializer

from django.http import Http404

from network.models import Connection

from django.shortcuts import get_object_or_404

from chat.serializer import ChatSerializer

from rest_framework import views

class ChatView(views.APIView):

    def get_chat(self, receiver_id, sender_id):
        try:
            chat1 = Chat.objects.filter(receiver = receiver_id, sender = sender_id )
            chat2 = Chat.objects.filter(receiver = sender_id, sender = receiver_id )
            return chat1 | chat2
        except:
            return Response({"detail":"No chat history found"}, status = status.HTTP_404_NOT_FOUND)
    
    def get(self, request, receiver_id):
        sender_id    = request.user.profile.id
        data = self.get_chat(receiver_id, sender_id)
        serializer = ChatSerializer(data, many = True, context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, receiver_id):
        sender    = request.user.profile
        receiver  = get_object_or_404(UserProfile, id = receiver_id)

        if (sender != receiver):
                data = request.data.copy()
                data['sender']    = sender.id
                data['receiver']  = receiver_id
                serializer = ChatSerializer(data = data, context = {'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"One can't send a message to himself"}, status = status.HTTP_403_FORBIDDEN)
        
        
class ChatDeleteView(views.APIView):
    def delete(self, request, chat_id):
        sender  = get_object_or_404(Chat, id = chat_id)
        request_user = request.user.profile
        if request_user == sender:
            query = Chat.objects.get(id = chat_id)
            query.delete()
            return Response({'detail':'Deleted chat successfully'}, status = status.HTTP_200_OK)
        return Response({'detail':"Can't delete chat history of others"}, status = status.HTTP_200_OK)
                                
                                

    
