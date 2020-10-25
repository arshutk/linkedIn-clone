from rest_framework import serializers

from userauth.models import User, UserProfile, UserExperience


        
        
class UserSerializer(serializers.ModelSerializer):
          
    class Meta:
        model   = User
        fields = ('id', 'email', 'password')
        extra_kwargs= {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password           = validated_data.pop('password')
        
        user = User(**validated_data)
        
        user.set_password(password)
        user.save()
        
        return user
    
class UserExperienceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = UserExperience
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
    

