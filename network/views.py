from django.shortcuts import render

from rest_framework import views, generics

from userauth.models import User, UserProfile

from userauth.serializers import UserSerializer, UserProfileSerializer

from network.models import Connection, Follow

from network.serializers import ConnectionSerializer, FollowSerializer

from rest_framework.response import Response

from django.http import Http404

from rest_framework import status

from rest_framework.permissions import AllowAny

from django.utils import timezone

from django.shortcuts import get_object_or_404

import json


class FollowView(views.APIView):
    def post(self, request, profile_id):
        user        = get_object_or_404(UserProfile, id = profile_id)
        follower    = request.user.profile
        
        if follower not in user.followers.all():
            serializer = FollowSerializer(data = {'user': user.id, 'follower': follower.id}, context = {'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'detail': "Follower added."}, status=status.HTTP_202_ACCEPTED) 
            return Response(serializer.errors, status=status.HTTP_202_ACCEPTED) 
        return Response({'detail': "Already followed."},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, profile_id):
        user        = get_object_or_404(UserProfile, id = profile_id)
        follower    = request.user.profile
        print(user.followers.all())
        if user.followers.filter(follower = follower):
            user.followers.get(follower = follower).delete()
            return Response({'detail': "User Unfollowed."},status=status.HTTP_201_CREATED) 
        return Response({'detail': "User is not followed."},status=status.HTTP_400_BAD_REQUEST)
  
    
class ConnectionSenderView(views.APIView):   
        
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
    def get_data(self, connections, user):
        data = list()
        for connection in connections:
            record   =  dict()
            record['connection_id'] = connection.id
            record['profile_id'] = getattr(connection, user).id
            record['profile_id'] = getattr(connection, user).id
            record['connection_name']   = f'{getattr(connection, user).first_name} {getattr(connection, user).last_name}'
            try:
                record['connection_avatar']   = self.request.build_absolute_uri(getattr(connection, user).avatar.url)
            except:
                record['connection_avatar'] = None
            record['connection_tagline']   = getattr(connection, user).social_profile.tagline
            time = timezone.localtime(timezone.now()) - connection.date_time 
            if time.days < 7:
                if time.days == 0:
                    record['time_elapsed'] = 'today'
                elif time.days == 1:
                    record['time_elapsed'] = 'yesterday'
                else:
                    record['time_elapsed'] = f'{time.days} days'
            elif time.days < 30:
                if int(time.days/7) == 1:
                    record['time_elapsed'] = '1 week'
                else:
                    record['time_elapsed'] = f'{int(time.days/7)} weeks'
            elif time.days < 365:
                if int(time.days/30) == 1:
                    record['time_elapsed'] = '1 month'
                else:
                    record['time_elapsed'] = f'{int(time.days/30)} months'
            else:
                if int(time.days/365) == 1:
                    record['time_elapsed'] = '1 year'
                else:
                    record['time_elapsed'] = f'{int(time.days/365)} years'
            data.append(record.copy())
        return data
        
    def get(self, request):
        user = get_object_or_404(UserProfile, id = request.user.profile.id)
        filter = self.request.query_params.get('filter')
        if filter == 'received':
            connections = Connection.objects.filter(receiver = user, has_been_accepted = False, is_visible = True)
            if connections.exists():
                response = self.get_data(connections, 'sender')
                return Response(response, status=status.HTTP_200_OK)
            return Response({'detail': "No request found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            if filter == 'sent':
                connections     = Connection.objects.filter(sender = user, has_been_accepted = False, is_visible = True)
                if connections.exists():
                    response = self.get_data(connections, 'receiver')
                    return Response(response, status=status.HTTP_200_OK)
                return Response({'detail': "No request found."}, status=status.HTTP_404_NOT_FOUND)
            else:    
                return Response({'detail': "Search with relevent filters."}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            connection_id       = request.data.get('connection_id')
            connection          = Connection.objects.get(id = connection_id)
        except:
            raise Http404
        user = request.user.profile
        if user == connection.receiver:  
            if not connection.has_been_accepted:
                connection.has_been_accepted = True
                connection.save()
                condition1 = user.followers.filter(follower = connection.sender).exists()
                condition2 = connection.sender.followers.filter(follower = user).exists()
                if not condition1 and not condition2:
                    Follow.objects.bulk_create([
                        Follow(user = user, follower = connection.sender),
                        Follow(user = connection.sender, follower = user)
                    ])
                else:
                    if not condition1:
                        Follow.objects.create(user = user, follower = connection.sender)
                    elif not condition2:
                        Follow.objects.create(user = connection.sender, follower = user)
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
                    connection.receiver.followers.get(follower = connection.sender).delete()
                    connection.sender.followers.get(follower = connection.receiver).delete()
                    connection.delete()
                    return Response({'detail': "Connection deleted"}, status=status.HTTP_204_NO_CONTENT)
                # connection.is_visible = False
                # connection.save()
                connection.delete()
                return Response({'detail': "Connection request has been removed."}, status=status.HTTP_202_ACCEPTED)
            if connection and connection.has_been_accepted: # For sender
                connection.receiver.followers.get(follower = connection.sender).delete()
                connection.sender.followers.get(follower = connection.receiver).delete()
                connection.delete()
                return Response({'detail': "Connection deleted"}, status=status.HTTP_204_NO_CONTENT)
            connection.delete()
            return Response({'detail': "Connection request deleted."}, status=status.HTTP_202_ACCEPTED)
        return Response({'detail': "Can't manage connections requests of which you arn't a part."}, status=status.HTTP_401_UNAUTHORIZED)
                

class NetworkView(views.APIView):
    def get_data(self, connection, query, user):
        del connection[user]
        connection['profile_id'] = getattr(query, user).id
        connection['connection_name'] = f'{getattr(query, user).first_name} {getattr(query, user).last_name}'
        try:
            connection['connection_avatar'] = self.request.build_absolute_uri(getattr(query, user).avatar.url)
        except:
            connection['connection_avatar'] = None
        connection['connection_tagline'] = getattr(query, user).social_profile.tagline
        return None
    
    def get(self, request):
        user    = get_object_or_404(UserProfile, id = request.user.profile.id)
        data    = Connection.objects.filter(sender = user, has_been_accepted = True) | Connection.objects.filter(receiver = user, has_been_accepted = True)
        connections  = ConnectionSerializer(data, many = True, context={'request': request}).data
        for connection in connections:
            query = Connection.objects.get(pk = connection['connection_id'])
            if connection['sender'] == user.id:
                self.get_data(connection, query, 'receiver')
            else:
                self.get_data(connection, query, 'sender')
        return Response(connections, status=status.HTTP_200_OK) 
    

