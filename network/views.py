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





class FollowView(views.APIView):
    
    
    def get_user(self, profile_id):
        try:
            return UserProfile.objects.get(id = profile_id)
        except:
            raise Http404
    
    def post(self, request, profile_id):
        user        = self.get_user(profile_id)
        follower    = request.user.profile
        
        if follower not in user.followers.all():
            user.followers.add(follower)
            return Response({'detail': "Follower added."}, status=status.HTTP_202_ACCEPTED) 
        return Response({'detail': "Already followed."},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, profile_id):
        user        = self.get_user(profile_id)
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
        receiver     = self.get_receiver(receiver_id)
        sender       = request.user.profile 
        
        try:
            if receiver.connections.get(sender = sender) and not receiver.connections.get(sender = sender).has_been_accepted:
                return Response({'detail': "You have already sent a request. Wait for it to get accepted."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'detail': "Already connected."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            if receiver is sender:
                data = dict()
                data['receiver'] = receiver_id
                data['sender'] = sender.id
                serializer = ConnectionSerializer(data = data, context = {'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response({'detail': "Can't connect with yourself."}, status = status.HTTP_400_BAD_REQUEST)
            
        
        
        
class PendingConnectionRequestView(views.APIView):
    
    def get_receiver(self, receiver_id):
        try:
            return UserProfile.objects.get(id = receiver_id)
        except:
            raise Http404
    
        
    def get(self, request):
        receiver        = self.get_receiver(request.user.profile.id)
        connections     = Connection.objects.filter(receiver = receiver, has_been_accepted = False, is_visible = True)
        if connections.exists():
            data = list()
            for connection in connections:
                record   =  dict()
                record['connection_id'] = connection.id
                record['sender_name']   = f'{connection.sender.first_name} {connection.sender.last_name}'
                record['description']   = f'{connection.sender.position} at {connection.sender.organization_name}'
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
        return Response({'detail': "No pending requests."}, status=status.HTTP_204_NO_CONTENT)
    
    
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
    
    def get_connection(self, connection_id):
        try:
            return Connection.objects.get(id = connection_id)
        except:
            raise Http404

    def delete(self, request, connection_id):
        connection       = self.get_connection(connection_id)
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
            if connection and connection.has_been_accepted: # For receiver
                connection.delete()
                connection.receiver.followers.delete(connection.sender)
                connection.sender.followers.delete(connection.receiver)
                return Response({'detail': "Connection deleted"}, status=status.HTTP_204_NO_CONTENT)
            connection.delete()
            return Response({'detail': "Connection request deleted."}, status=status.HTTP_202_ACCEPTED)
        return Response({'detail': "Can't manage connections requests of which you arn't a part."}, status=status.HTTP_401_UNAUTHORIZED)
                

class NetworkView(views.APIView):
    
    def get_user(self, profile_id):
        try:
            return UserProfile.objects.get(id = profile_id)
        except:
            raise Http404
    
    def get(self, request):
        user        = self.get_user(request.user.profile.id)
        data        = Connection.objects.filter(sender = user, has_been_accepted = True) | Connection.objects.filter(receiver = user, has_been_accepted = True)
        serializer  = ConnectionSerializer(data, many = True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED) 
    

