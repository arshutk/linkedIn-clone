from rest_framework import serializers, exceptions, fields

from profile.models import WorkExperience, Education, LicenseAndCertification, VolunteerExperience, Course, Project,\
                           TestScore, Skill, SocialProfile, ProfileView, JobVacancy, JobApplication

from userauth.models import User, UserProfile

from userauth.serializers import UserProfileSerializer

from rest_framework import status 

import json


class WorkExperienceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = WorkExperience
        fields  = '__all__'  
           
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data['id']
        return response
    
    
    
class EducationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Education
        fields  = '__all__' 
              
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data['id']
        return response



class LicenseAndCertificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = LicenseAndCertification
        fields  = '__all__'
          
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        return response
    
    
class VolunteerExperienceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = VolunteerExperience
        fields  = '__all__'
             
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        return response
    
    

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Course
        fields  = '__all__'
              
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        return response
    

class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Project
        fields  = '__all__'
              
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        return response
    
    
class TestScoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = TestScore
        fields  = '__all__'
              
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        return response
  
  
    
from profile.models import SKILLS

class SkillSerializer(serializers.ModelSerializer):
    
    # skills_list        = fields.MultipleChoiceField(choices = SKILLS)   
    class Meta:
        model   = Skill
        fields  = '__all__'
              
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data['id']
        response['top_skills'] = json.decoder.JSONDecoder().decode(instance.top_skills)
        # Temporary (remove later)
        response['skills_list'] = json.decoder.JSONDecoder().decode(instance.skills_list)
        return response
    
    
class SocialProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = SocialProfile
        fields  = '__all__'
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        # response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        response['current_industry'] = WorkExperienceSerializer(instance.current_industry, context = {'request': self.context.get('request')}).data['organization_name']
        response['current_academia'] = EducationSerializer(instance.current_academia, context = {'request': self.context.get('request')}).data['organization_name']
        return response
    
    
class ProfileViewSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model   = ProfileView
        fields  = '__all__'
        
    # def to_representation(self,instance):
        # response = super().to_representation(instance)
        # response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        # response['profile'] = SocialProfileSerializer(instance.profile, context = {'request': self.context.get('request')}).data
        # return response
        
class JobVacanySerializer(serializers.ModelSerializer):

    class Meta:
        model   = JobVacancy
        fields  = '__all__'
    
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['saved_by'] = UserProfileSerializer(instance.saved_by, many = True, context = {'request': self.context.get('request')}).data
        response['viewed_by'] = UserProfileSerializer(instance.viewed_by, many = True, context = {'request': self.context.get('request')}).data
        response['applicants'] = UserProfileSerializer(instance.applicants, many = True, context = {'request': self.context.get('request')}).data
        return response


class JobApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model   = JobApplication
        fields  = '__all__'