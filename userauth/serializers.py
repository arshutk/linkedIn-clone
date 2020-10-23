from rest_framework import serializers

from userauth.models import User, UserProfile, UserExperience

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = UserProfile
        fields  = ('first_name', 'last_name', 'avatar', 'location')
    
    
class UserExperienceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = UserExperience
        fields  = ('name', 'category', 'position', 'start_year', 'end_year')
    

class UserSerializer(serializers.ModelSerializer):
    
    profile         = UserProfileSerializer(required=True)
    experience      = UserExperienceSerializer(required=True)
    
    class Meta:
        model   = User
        fields = ('email', 'password', 'profile', 'experience')
        extra_kwargs= {'password': {'write_only': True}}
    
    def create(self, validated_data):
        profile_data       = validated_data.pop('profile')
        experience_data    = validated_data.pop('experience')
        password           = validated_data.pop('password')
        
        user = User(**validated_data)
        
        user.set_password(password)
        user.save()
        print(profile_data)
        print(experience_data)
        UserProfile.objects.create(user = user,**profile_data)
        UserExperience.objects.create(user = user,**experience_data)
        
        return user
    
# {"email": "aqq@a.com","password":"qwerty", "profile": {"first_name": "first", "last_name": "sec", "location": "allahabad"}, "experience": {"name": "DeveloperHUb", "category": "Student", "position": "dev", "start_year": "2020-09-12", "end_year": "2021-09-12"}}