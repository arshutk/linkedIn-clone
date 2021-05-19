from rest_framework import serializers, exceptions

from userauth.models import User, UserProfile

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from userauth import views

import json

from rest_framework import status 

from network.models import Connection


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
            # if user.check_password(password): 
            user.profile
        except:
            raise exceptions.NotFound("User has not filled his details & is also not verified.") #404
        
        if user.active:
            if user.check_password(password):
                data = super(MyTokenObtainPairSerializer, self).validate(attrs)
                data.update({'profile_id': self.user.profile.id})
                # try:
                #     domain_name = self.context["request"].META['HTTP_HOST']
                #     picture_url = self.user.profile.avatar.url
                #     absolute_url = 'http://' + domain_name + picture_url
                #     data.update({'avatar': absolute_url})
                # except:
                #     data.update({'avatar': None})
                # data.update({'first_name': self.user.profile.first_name})
                # data.update({'last_name': self.user.profile.last_name})
                # data.update({'tagline': self.user.profile.social_profile.tagline})
                # data.update({'connection': self.user.profile.last_name})
                # connection          = Connection.objects.filter(sender = self.user.profile, has_been_accepted = True).count() + \
                #                       Connection.objects.filter(receiver = self.user.profile, has_been_accepted = True).count()
                # data.update({'connection' : connection})
                # data.update({'profile_views': 0})  
                data.update({'about_id': self.user.profile.social_profile.id})
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
 
         
    
class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = UserProfile
        fields  = '__all__'
        

class UserProfileSearchSerailizer(serializers.Serializer):
    profile_id = serializers.CharField(source = 'id')
    
    class Meta:
        model = UserProfile
        fields = ('profile_id')
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['name'] = f'{instance.first_name} {instance.last_name}'
        response['avatar'] = self.get_avatar(instance)
        response['tagline'] = instance.social_profile.tagline
        return response    
    
    def get_avatar(self, instance):
        try:
            name = instance.avatar.url
            url = self.context['request'].build_absolute_uri(name)
            return url
        except:
            return None
    