from django.shortcuts import render

from rest_framework import views, generics

from userauth.serializers import UserSerializer, UserProfileSerializer, UserExperienceSerializer

from userauth.models import User, UserProfile, UserExperience, OTPModel

from rest_framework.response import Response

from django.http import Http404

from rest_framework import status

from rest_framework.permissions import AllowAny

import time

from random import randint

def OTP_create(email_linked, phone_linked):
    OTPModel.objects.filter(email_linked__iexact = email_linked).delete()
    
    otp = randint(100000, 999999) 
    time_of_creation = int(time.time())
    OTPModel.objects.create(otp = otp, email_linked = email_linked, phone_linked = phone_linked, time_created = time_of_creation) 
    return None  


class UserCreateView(views.APIView):
    serializer_class = UserSerializer

    def post(self, request): 
        serializer = UserSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_201_CREATED)
    
    


class UserProfileCreateView(views.APIView):
    serializer_class = UserProfileSerializer
        
    def post(self, request, user_id):
        data = request.data.copy()
        data['user'] = user_id
        
        serializer = UserProfileSerializer(data = data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_201_CREATED)
    
class UserProfileView(views.APIView):
    serializer_class = UserProfileSerializer
    
    def get(self, request, profile_id):
        try:
            user = UserProfile.objects.get(id=profile_id)
        except:
            raise Http404
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)
            
        
    def patch(self, request, profile_id):
        try:
            user = UserProfile.objects.get(id = profile_id)
            data = request.data.copy()
        except:
            raise Http404
        
        phone_linked    = data.get('phone_number')
        email_linked    = User.objects.get(profile = user).email
        OTP_create(email_linked, phone_linked)
        serializer = UserProfileSerializer(user, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

     
class UserExperienceCreateView(views.APIView):
    serializer_class = UserExperienceSerializer
    
    def post(self, request):
        serializer = UserExperienceSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_201_CREATED)

  
class AccountVerificationView(views.APIView):
    
    def post(self, request):
        data = request.data.copy()
        
        request_phone_linked = data.get('phone_number')
        request_OTP_code     = data.get('otp')
        current_time         = int(time.time())
        
        try:
            query = OTPModel.objects.get(phone_linked = request_phone_linked)
        except:
            raise Http404
        
        generated_otp      = query.otp
        registered_phone   = query.phone_linked 
        time_created       = query.time_created
        
        if registered_phone == request_phone_linked:
            if generated_otp == request_OTP_code: 
                if current_time - time_created < 300: # 5 Minutes
                    user  =  User.objects.get(email__iexact = query.email_linked)
                    user.active = True
                    user.save()
                    OTPModel.objects.filter(email_linked__iexact = query.email_linked).delete()
                    return Response({'detail':'TEST MESSAGE'}, status = status.HTTP_201_CREATED)
                return Response({'detail':'TEST MESSAGE'}, status = status.HTTP_201_CREATED)
            return Response({'detail':'TEST MESSAGE'}, status = status.HTTP_201_CREATED)
        return Response({'detail':'TEST MESSAGE'}, status = status.HTTP_201_CREATED)
                
     
    
    
        
        
