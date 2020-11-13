from django.shortcuts import render

from rest_framework import views, generics

from userauth.serializers import UserSerializer, UserProfileSerializer, MyTokenObtainPairSerializer

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

########################do bar post ho rha
    serializer_class = UserProfileSerializer
    
    def get_user(self, profile_id):
        try:
            return UserProfile.objects.get(id = profile_id)
        except:
            raise Http404
    
    def get_work_experience(self, work_id):
        try:
            return WorkExperience.objects.get(id = work_id)
        except:
            raise Http404
        
    def get_academic_experience(self, academic_id):
        try:
            return Education.objects.get(id = academic_id)
        except:
            raise Http404
        
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
                job_serializer  = WorkExperienceSerializer(data = job_data, context = {'request': request})
                if job_serializer.is_valid():
                    job_serializer.save()
                    SocialProfile.objects.create(user = self.get_user(serializer.data['id']), 
                                                 headline = f"{serializer.data['position']} at {serializer.data['organization_name']}",
                                                 current_work_organization = self.get_work_experience(job_serializer.data['id']))
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(job_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            
            study_data = dict()
            study_data['user'] = serializer.data['id']
            study_data['organization_name'] = data['organization_name']
            try:
                    job_data['start_date'] = data['start_date']
            except:
                pass
            study_data['end_date'] = data.get('end_date')
            study_serializer  = EducationSerializer(data = study_data, context = {'request': request})
            if study_serializer.is_valid():
                study_serializer.save()
                SocialProfile.objects.create(user = self.get_user(serializer.data['id']), 
                                             headline = f"{serializer.data['position']} at {serializer.data['organization_name']}",
                                             current_academic_organization = self.get_academic_experience(study_serializer.data['id']))
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(study_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
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
        
