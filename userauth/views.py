from django.shortcuts import render

from rest_framework import views, generics

from userauth.serializers import UserSerializer, UserProfileSerializer, MyTokenObtainPairSerializer, UserJobExperienceSerializer, UserStudyExperienceSerializer, ConnectionSerializer, ConnectionSerializer

from userauth.models import User, UserProfile, OTPModel, UserJobExperience, UserStudyExperience, Connection

from rest_framework.response import Response

from django.http import Http404

from rest_framework import status

from rest_framework.permissions import AllowAny

import time

from random import randint

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone

    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




def OTP_create_send(email_linked, phone_linked):
    OTPModel.objects.filter(email_linked__iexact = email_linked).delete()
    otp = randint(100000, 999999) 
    while OTPModel.objects.filter(otp = otp):
        otp = randint(100000, 999999)
    time_of_creation = int(time.time())
    OTPModel.objects.create(otp = otp, email_linked = email_linked, phone_linked = phone_linked, time_created = time_of_creation)   
    
                                                        ##############
                                                        # SMS CODE   #    
                                                        ##############
                                                        
    return None  



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class UserCreateView(views.APIView):
    permission_classes = [AllowAny]

    serializer_class = UserSerializer

    def post(self, request):
        try:
            User.objects.get(email__iexact = request.data['email'])
            return Response({'detail':'User with this email already exists'}, status = status.HTTP_226_IM_USED)
        except:
            serializer = UserSerializer(data = request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, user_id = None):
        
        try:
            data                = request.data.copy()
            user_id             = data.get('user_id')
            new_password        = data.get('password')
            user                = User.objects.get(id = user_id)
        except:
            raise Http404
        
        if request.user == User.objects.get(pk = user_id):
            if new_password:
                if not user.check_password(new_password):   
                    user.set_password(new_password)
                    user.save()
                    return Response({'detail':'Password changed successfully'}, status = status.HTTP_202_ACCEPTED)
                return Response({'detail':'Password is same as old.'},status = status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'detail':'Password must not be null'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'You can\'t change password of other users.' },status = status.HTTP_401_UNAUTHORIZED)


class UserProfileCreateView(views.APIView):
    permission_classes = [AllowAny]


########################do bar post ho rha
    serializer_class = UserProfileSerializer
        
    def post(self, request, user_id):
        data = request.data.copy()
        data['user'] = user_id

        serializer = UserProfileSerializer(data = data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            if data.get('is_employed'):
                job_data = dict()
                job_data['user'] = serializer.data['id']
                job_data['organization_name'] = data['organization_name']
                job_data['position'] = data['position']
                try:
                    job_data['start_date'] = data['start_date']
                except:
                    pass
                job_data['end_date'] = data.get('end_date')
                job_serializer  = UserJobExperienceSerializer(data = job_data, context = {'request': request})
                if job_serializer.is_valid():
                    job_serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(job_serializer.errors, status = status.HTTP_201_CREATED)
            study_data = dict()
            print('school')
            study_data['user'] = serializer.data['id']
            study_data['organization_name'] = data['organization_name']
            try:
                    job_data['start_date'] = data['start_date']
            except:
                pass
            study_data['end_date'] = data.get('end_date')
            study_serializer  = UserStudyExperienceSerializer(data = study_data, context = {'request': request})
            if study_serializer.is_valid():
                study_serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(study_serializer.errors, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_201_CREATED)
    
    
    def patch(self, request, user_id = None):
        
        try:
            data                = request.data.copy()
            profile_id          = data['profile_id']
            user                = UserProfile.objects.get(id = profile_id)
        except:
            raise Http404
        
        phone_linked            = data.get('phone_number')
        queryset                = OTPModel.objects.filter(phone_linked = phone_linked)
    
        if not queryset.exists():
            email_linked    = User.objects.get(profile = user).email
            OTP_create_send(email_linked, phone_linked)
            serializer = UserProfileSerializer(user, data = data, partial = True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Phone number already in use.'}, status = status.HTTP_401_UNAUTHORIZED)
    
    
  
    
class UserProfileView(views.APIView):
    serializer_class = UserProfileSerializer
    
    
    def get(self, request, profile_id):
        try:
            user = UserProfile.objects.get(id=profile_id)
        except:
            raise Http404
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)
            
        


  
class OTPVerificationView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data.copy()
        
        request_phone        = data.get('phone_number')
        request_OTP_code     = data.get('otp')
        current_time         = int(time.time())
  
        try:
            query = OTPModel.objects.get(phone_linked = request_phone)
        except:
            raise Http404
        
        generated_otp      = query.otp
        time_created       = query.time_created
        
        if generated_otp == request_OTP_code: 
            if current_time - time_created < 300: # 5 Minutes
                user  =  User.objects.get(email__iexact = query.email_linked)
                user.active = True
                user.save()
                query.delete()
                return Response(get_tokens_for_user(user), status = status.HTTP_200_OK)
            return Response({'detail':'OTP expired. Request for OTP again.'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Wrong OTP Entered.'}, status = status.HTTP_403_FORBIDDEN)
                   
    
    
                     
                
class OTPSend(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        request_phone_number = request.data.get("phone_number","")
        
        try:
            user         = UserProfile.objects.get(phone_number = request_phone_number)
            email_linked = user.user.email
            user_id      = user.user.id
        except:
            return Response({'detail':'User not found'} ,status = status.HTTP_404_NOT_FOUND)

        if request_phone_number:
            OTP_create_send(email_linked, request_phone_number)
            return Response({'user_id': user_id}, status = status.HTTP_202_ACCEPTED)
        
        
        
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
    
    
    def get_reciever(self, receiver_id):
        try:
            return UserProfile.objects.get(id = receiver_id)
        except:
            raise Http404
        
        
    def post(self, request, receiver_id):
        receiver     = self.get_reciever(receiver_id)
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
    
    def get_reciever(self, receiver_id):
        try:
            return UserProfile.objects.get(id = receiver_id)
        except:
            raise Http404
    
        
    def get(self, request):
        receiver        = self.get_reciever(request.user.profile.id)
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
                return Response({'detail':'User added to your network.'}, status = status.HTTP_202_ACCEPTED)
            return Response({'detail':'User already added to your network.'}, status = status.HTTP_202_ACCEPTED)
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
 
        # try:
        #     if connection and connection.has_been_accepted:
        #         connection.delete()
        #         return Response({'detail': "Connection deleted"}, status=status.HTTP_202_ACCEPTED)
        #     connection.delete()
        #     return Response({'detail': "Connection request deleted"}, status=status.HTTP_202_ACCEPTED)
        # except:
        #     return Response({'detail': "You arn't connected to user."}, status = status.HTTP_400_BAD_REQUEST)  
        if requesting_user == sender or requesting_user == receiver: 
            if receiver == requesting_user:
                if connection and connection.has_been_accepted:
                    connection.delete()
                    return Response({'detail': "Connection deleted"}, status=status.HTTP_202_ACCEPTED)
                connection.is_visible = False
                connection.save()
                return Response({'detail': "Connection request has been removed."}, status=status.HTTP_202_ACCEPTED)
            if connection and connection.has_been_accepted: # For receiver
                connection.delete()
                return Response({'detail': "Connection deleted"}, status=status.HTTP_202_ACCEPTED)
            connection.delete()
            return Response({'detail': "Connection request deleted."}, status=status.HTTP_202_ACCEPTED)
        return Response({'detail': "Can't manage connections requests of which you arn't a part."}, status=status.HTTP_202_ACCEPTED)
                
    
        
        
        
        
# class ConnectionReceiverView(views.APIView):
    
#     def get_reciever(self, receiver_id):
#         try:
#             return UserProfile.objects.get(id = receiver_id)
#         except:
#             raise Http404
        
#     def get_reciever(self, receiver_id):
#         try:
#             return UserProfile.objects.get(id = receiver_id)
#         except:
#             raise Http404
        
#     def get_connections(self, connection_id):
#         try:
#             return Connection.objects.get(id = connection_id)
#         except:
#             raise Http404    
        
        
#     def post(self, request, connection_id):
#         pass
      

        