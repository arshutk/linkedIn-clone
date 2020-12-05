from django.shortcuts import render

from rest_framework import views, generics

from userauth.serializers import UserSerializer, UserProfileSerializer, MyTokenObtainPairSerializer, UserProfileSearchSerailizer

from userauth.models import User, UserProfile, OTPModel

from profile.models import WorkExperience, Education, SocialProfile

from profile.serializers import WorkExperienceSerializer, EducationSerializer, SocialProfileSerializer

from rest_framework.response import Response

from django.http import Http404

from rest_framework import status

from rest_framework.permissions import AllowAny

import time

from random import randint

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone

from network.models import Connection

from rest_framework import filters

from django.core.mail import send_mail
    
from django.template import loader


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
    # html_content = loader.render_to_string('index.html', context = {'otp' : otp,})
    # mail_body = f"OTP is {otp}. This OTP will be valid for 5 minutes."
    # send_mail('Greetings from SmartLearn Team', mail_body, 'LinkedInClone<utkp09@gmail.com>', [email_linked], html_message = html_content, fail_silently = False)                                                    
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
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request):
        
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
                return Response({'detail':'Password is same as old.'}, status = status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'detail':'Password must not be null'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'You can\'t change password of other users.' },status = status.HTTP_401_UNAUTHORIZED)


class UserProfileCreateView(views.APIView):
    permission_classes = [AllowAny]

    serializer_class = UserProfileSerializer
    
    def get_user(self, profile_id):
        try:
            return UserProfile.objects.get(id = profile_id)
        except:
            raise Http404
    
    def get_industry(self, profile_id):
        try:
            return WorkExperience.objects.get(user = profile_id)
        except:
            raise Http404
        
    def get_academia(self, profile_id):
        try:
            return Education.objects.get(user = profile_id)
        except:
            raise Http404
        
    def post(self, request, user_id):
        data = request.data.copy()
        data['user'] = user_id
        serializer = UserProfileSerializer(data = data, context={'request': request})
        if serializer.is_valid(): 
            serializer.save()
            if data.get('is_employed') == 'true':
                print('here')
                WorkExperience.objects.create(user = self.get_user(serializer.data['id']), 
                                             organization_name = f"{data['organization_name']}", 
                                             position = data['position'], 
                                             start_date = data['start_date'], 
                                             end_date = data['end_date'])
                
                SocialProfile.objects.create(user = self.get_user(serializer.data['id']), 
                                                tagline = f"{data['position']} at {data['organization_name']}",
                                                current_industry = self.get_industry(serializer.data['id']))                                
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            Education.objects.create(user = self.get_user(serializer.data['id']), 
                                             organization_name = f"{data['organization_name']}",
                                             start_date = data['start_date'],
                                             end_date = data['end_date'])
                                             
            SocialProfile.objects.create(user = self.get_user(serializer.data['id']), 
                                            tagline = f"{data['position']} at {data['organization_name']}",
                                            current_academia = self.get_academia(serializer.data['id']))
            return Response(serializer.data, status = status.HTTP_201_CREATED)
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
        return Response({'detail':'Phone number already in use.'}, status = status.HTTP_403_FORBIDDEN)
    
    
  
    
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
        

class UserInfo(views.APIView):
    
    def get(self, request):
        user = request.user.profile
        
        user_name = f'{user.first_name} {user.last_name}'
        try:
            user_avatar  = request.build_absolute_uri(user.avatar.url)
        except:
            user_avatar = None
        user_tagline = user.social_profile.tagline
        connection   = Connection.objects.filter(sender = user, has_been_accepted = True).count() + \
                       Connection.objects.filter(receiver = user, has_been_accepted = True).count()
        bookmarks    = user.bookmarked_posts.count()
        
        return Response({'user_name': user_name,
                        'user_avatar': user_avatar,
                        'user_tagline': user_tagline,
                        'connection': connection,
                        'bookmarks': bookmarks}, status = status.HTTP_200_OK)
                               

# Search

class UserSearchView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSearchSerailizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name','location',]
    
    # def get_serializer_context(self):
    #     # print(self.request.query_params.get('radius'))
    #     context = super(JobSearchView, self).get_serializer_context()
    #     context.update({"request": self.request, 'user': self.request.user.profile})
    #     return context
    
class ProfileRecommendView(views.APIView):
    def get(self, request):
        user = request.user.profile
        query = UserProfile.objects.exclude(id = user.id).order_by('?')[:10]
        serializer = UserProfileSearchSerailizer(query, many = True, context = {'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)
        
                

