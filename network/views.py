from django.shortcuts import render

from rest_framework import views, generics

from userauth.models import User, UserProfile
from userauth.serializers import UserSerializer, UserProfileSerializer

from network.models import Connection

from network.serializers import ConnectionSerializer

from rest_framework.response import Response

from django.http import Http404

from rest_framework import status

from rest_framework.permissions import AllowAny

from django.utils import timezone

from django.shortcuts import get_object_or_404

import json


class FollowView(views.APIView):
    
    
    def get_user(self, profile_id):
        try:
            return UserProfile.objects.get(id = profile_id)
        except:
            raise Http404
    
    def post(self, request, profile_id):
        user        = get_object_or_404(UserProfile, id = profile_id)
        follower    = request.user.profile
        
        if follower not in user.followers.all():
            user.followers.add(follower)
            return Response({'detail': "Follower added."}, status=status.HTTP_202_ACCEPTED) 
        return Response({'detail': "Already followed."},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, profile_id):
        user        = get_object_or_404(UserProfile, id = profile_id)
        follower    = request.user.profile
 
        if user in user.followers.all():
            user.followers.remove(follower)
            return Response({'detail': "User Unfollowed."},status=status.HTTP_201_CREATED) 
        return Response({'detail': "User is not followed."},status=status.HTTP_400_BAD_REQUEST)
  
    
class ConnectionSenderView(views.APIView):   
    
    def get_receiver(self, receiver_id):
        try:
            return UserProfile.objects.get(id = receiver_id)
        except:
            raise Http404
        
        
    def post(self, request, receiver_id):
        receiver     = get_object_or_404(UserProfile, id = receiver_id)
        sender       = request.user.profile 
        
        try:
            if receiver.request_received.get(sender = sender) and not receiver.request_received.get(sender = sender).has_been_accepted:
                return Response({'detail': "You have already sent a request. Wait for it to get accepted."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'detail': "Already connected."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            if receiver != sender:
                data = dict()
                data['receiver'] = receiver_id
                data['sender'] = sender.id
                serializer = ConnectionSerializer(data = data, context = {'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response({'detail': "Can't connect with yourself."}, status = status.HTTP_226_IM_USED)
            
       
class PendingConnectionRequestView(views.APIView):   
        
    def get(self, request, filter):
        receiver     = get_object_or_404(UserProfile, id = request.user.profile.id)
        if filter == 'received':
            connections     = Connection.objects.filter(receiver = receiver, has_been_accepted = False, is_visible = True)
            if connections.exists():
                data = list()
                for connection in connections:
                    record   =  dict()
                    record['connection_id'] = connection.id
                    record['profile_id'] = connection.sender.id
                    record['sender_name']   = f'{connection.sender.first_name} {connection.sender.last_name}'
                    record['sender_avatar']   = request.build_absolute_uri(connection.sender.avatar.url)
                    record['sender_tagline']   = connection.sender.social_profile.tagline
        else:
            if filter == 'sent':
                connections     = Connection.objects.filter(sender = receiver, has_been_accepted = False, is_visible = True)
                if connections.exists():
                    data = list()
                    for connection in connections:
                        record   =  dict()
                        record['connection_id'] = connection.id
                        record['profile_id'] = connection.receiver.id
                        record['receiver_name']   = f'{connection.receiver.first_name} {connection.receiver.last_name}'
                        record['receiver_avatar']   = request.build_absolute_uri(connection.receiver.avatar.url)
                        record['receiver_tagline']   = connection.receiver.social_profile.tagline
            else:
                return Response({'detail': "Given search query is not acceptable."}, status=status.HTTP_400_BAD_REQUEST)
            time = timezone.localtime(timezone.now()) - connection.date_time 
            if time.days < 7:
                if time.days == 0:
                    record['time_elapsed'] = 'today'
                elif time.days == 1:
                    record['time_elapsed'] = 'yesterday'
                else:
                    record['time_elapsed'] = f'{time.days} days'
            elif time.days < 30:
                if time.days % 7 == 1:
                    record['time_elapsed'] = '1 week'
                else:
                    record['time_elapsed'] = f'{time.days % 7} weeks'
            elif time.days < 365:
                if time.days % 30 == 0:
                    record['time_elapsed'] = '1 month'
                else:
                    record['time_elapsed'] = f'{time.days % 30} weeks'
            else:
                if time.days % 365 == 0:
                    record['time_elapsed'] = '1 year'
                else:
                    record['time_elapsed'] = f'{time.days % 365} years'
            data.append(record.copy())
            return Response(data, status=status.HTTP_200_OK)
        return Response({'detail': "No requests found."}, status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request):
        try:
            connection_id       = request.data.get('connection_id')
            connection          = Connection.objects.get(id = connection_id)
        except:
            raise Http404
        if request.user.profile == connection.receiver:  
            if not connection.has_been_accepted:
                connection.has_been_accepted = True
                connection.save()
                connection.receiver.followers.add(connection.sender)
                connection.sender.followers.add(connection.receiver)
                return Response({'detail':'User added to your network.'}, status = status.HTTP_201_CREATED)
            return Response({'detail':'User already added to your network.'}, status = status.HTTP_226_IM_USED)
        return Response({'detail':'You can\'t manage network of other users.' },status = status.HTTP_401_UNAUTHORIZED)        
 
class ConnectionDeleteView(views.APIView):

    def delete(self, request, connection_id):
        connection       = get_object_or_404(Connection, id = connection_id)
        receiver         = connection.receiver
        sender           = connection.sender
        requesting_user  = request.user.profile
 
        if requesting_user == sender or requesting_user == receiver: 
            if receiver == requesting_user:
                if connection and connection.has_been_accepted:
                    connection.delete()
                    connection.receiver.followers.delete(connection.sender)
                    connection.sender.followers.delete(connection.receiver)
                    return Response({'detail': "Connection deleted"}, status=status.HTTP_204_NO_CONTENT)
                connection.is_visible = False
                connection.save()
                return Response({'detail': "Connection request has been removed."}, status=status.HTTP_202_ACCEPTED)
            if connection and connection.has_been_accepted: # For sender
                connection.delete()
                connection.receiver.followers.delete(connection.sender)
                connection.sender.followers.delete(connection.receiver)
                return Response({'detail': "Connection deleted"}, status=status.HTTP_204_NO_CONTENT)
            connection.delete()
            return Response({'detail': "Connection request deleted."}, status=status.HTTP_202_ACCEPTED)
        return Response({'detail': "Can't manage connections requests of which you arn't a part."}, status=status.HTTP_401_UNAUTHORIZED)
                

class NetworkView(views.APIView):
    
    def get(self, request):
        user    = get_object_or_404(UserProfile, id = request.user.profile.id)
        data    = Connection.objects.filter(sender = user, has_been_accepted = True) | Connection.objects.filter(receiver = user, has_been_accepted = True)
        connections  = ConnectionSerializer(data, many = True, context={'request': request}).data
        for connection in connections:
            query = Connection.objects.get(pk = connection['id'])
            if connection['sender'] == user.id:
                del connection['receiver']
                connection['sender_name'] = f'{query.receiver.first_name} {query.receiver.last_name}'
                connection['sender_avatar'] = request.build_absolute_uri(query.receiver.avatar.url)
                connection['sender_tagline'] = query.receiver.social_profile.tagline
            else:
                del connection['sender']    
                connection['receiver_name'] = f'{query.sender.first_name} {query.sender.last_name}'
                connection['receiver_avatar'] = request.build_absolute_uri(query.sender.avatar.url)
                connection['receiver_tagline'] = query.sender.social_profile.tagline
        return Response(connections, status=status.HTTP_200_OK) 
    

