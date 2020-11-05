from rest_framework import serializers, exceptions

from userprofile.models import WorkExperience, Education

from userauth.models import User, UserProfile

from userauth.serializers import UserProfileSerializer

from rest_framework import status 




class WorkExperienceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = WorkExperience
        fields  = '__all__'
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        return response
    
class EducationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Education
        fields  = '__all__'
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        return response