from rest_framework import serializers, exceptions

from userauth.models import User, UserProfile, UserJobExperience, UserStudyExperience, Connection

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from userauth import views

import json

from rest_framework.response import Response
from rest_framework import status 


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        request = self.context["request"].data
        data = json.dumps(request)
        request_data = json.loads(data)

        email = request_data.get("email","")
        password = request_data.get("password","")
        
        try:
            user = User.objects.get(email__iexact = email)
        except:
            raise exceptions.ParseError("User with entered email doesn't exists.")   #400
        
        try:
            if user.check_password(password): 
                user.profile
        except:
            raise exceptions.NotFound("User has not filled his details & is also not verified.") #404
        
        if user.active:
            if user.check_password(password):
                data = super(MyTokenObtainPairSerializer, self).validate(attrs)
                data.update({'email': self.user.email})
                data.update({'is_employed' : self.user.profile.is_employed})
                data.update({'organization_name' : self.user.profile.organization_name})
                data.update({'position' : self.user.profile.position})
                try:
                    domain_name = self.context["request"].META['HTTP_HOST']
                    picture_url = self.user.profile.avatar.url
                    absolute_url = 'http://' + domain_name + picture_url
                    data.update({'picture': absolute_url})
                except:
                    data.update({'picture': None})
                self.user.profile.is_online = True
                data.update({'is_online': self.user.profile.is_online})
                return data                                                          #200
            raise exceptions.AuthenticationFailed("Entered password is wrong")       #401
        # views.OTP_create_send(self.user.email, self.user.profile.phone_number)
        raise exceptions.PermissionDenied("User is registered but not verified")     #403
    
    
        
class UserSerializer(serializers.ModelSerializer):
          
    class Meta:
        model   = User
        fields = ('id', 'email', 'password')
        extra_kwargs= {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password  = validated_data.pop('password')
        
        user = User(**validated_data)
        
        user.set_password(password)
        user.save()
        
        return user
    
class UserJobExperienceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = UserJobExperience
        fields  = '__all__'
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        return response
    
class UserStudyExperienceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = UserStudyExperience
        fields  = '__all__'
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        return response
 
          
    
class UserProfileSerializer(serializers.ModelSerializer):

    
    class Meta:
        model   = UserProfile
        fields  = '__all__'
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user, context = {'request': self.context.get('request')}).data
        return response
   
   
   
class ConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Connection
        fields  = '__all__'   
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['sender'] = UserProfileSerializer(instance.sender, context = {'request': self.context.get('request')}).data
        response['receiver'] = UserProfileSerializer(instance.receiver, context = {'request': self.context.get('request')}).data
        return response

