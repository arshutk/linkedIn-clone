from rest_framework import serializers, exceptions, fields

from profile.models import WorkExperience, Education, LicenseAndCertification, VolunteerExperience, Course, Project,\
                           TestScore, Skill, Endorsement, SocialProfile, ProfileView, JobVacancy, JobApplication

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
  
class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Skill
        fields  = '__all__'

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
    
# class SkillSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model   = Skill
#         fields  = ('id',)
              
#     def to_representation(self,instance):
#         response = super().to_representation(instance)
#         response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data['id']
#         response['top_skills'] = json.decoder.JSONDecoder().decode(instance.top_skills)
#         response['skills_list'] = self.get_skills_list(instance)
#         return response
    
#     def get_skills_list(self, instance):
#         skills_list = json.decoder.JSONDecoder().decode(instance.skills_list)
#         endorsed_skill = instance.endorsements.values_list('skill_name', flat = True).distinct()
#         a = list()
#         for skill in skills_list:
#             if skill in endorsed_skill:
#                 query = instance.endorsements.filter(skill_name = skill)
#                 serializer = GetEndorsementSerializer(query, many = True, context = {'request': self.context.get('request')})
#                 a.append({skill : serializer.data})
#             else:
#                 a.append({skill : None})
#         return a
    

class EndorsementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Endorsement
        fields  = '__all__'    
        
        
class GetEndorsementSerializer(serializers.ModelSerializer):
    endorsement_id = serializers.CharField(source = 'id')
    
    class Meta:
        model   = Endorsement
        fields  = ('endorsement_id',)    
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['endorser_id'] = instance.user.id
        response['endorser_name'] = f'{instance.user.first_name} {instance.user.last_name}'
        response['endorser_tagline'] = instance.user.social_profile.tagline
        response['endorser_avatar'] = self.get_endorser_avatar(instance)
        return response         
        
    def get_endorser_avatar(self, instance):
        try:
            name = instance.user.avatar.url
            url  = self.context['request'].build_absolute_uri(name)
            return url
        except:
            return None
    
    
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
        
class JobVacanySerializer(serializers.ModelSerializer):
    vacancy_id = serializers.CharField(source = 'id')

    class Meta:
        model   = JobVacancy
        fields  = ('vacancy_id', 'title', 'organization', 'location','employment_type',
                   'description', 'skills_required', 'posted_at', 'industry',
                   'pay_range','file_linked', 'description',)
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['num_of_applicants'] = instance.applicants.count()
        response['applicants'] = self.get_applicants_info(instance)
        response['is_my_posted_vacancy'] = self.context['user'] == instance.posted_by
        response['is_bookmarked'] = self.context['user'] in instance.saved_by.all()
        response['has_applied'] = self.context['user'] in instance.applicants.all()
        return response
    
    def get_applicants_info(self, instance):
        applicants = instance.applicants.all()
        response = list()
        for applicant in applicants:
            applicant_id = applicant.id
            applicant_name = f'{applicant.first_name} {applicant.last_name}'
            applicant_avatar = self.get_applicant_avatar(instance)
            applicant_tagline = applicant.social_profile.tagline
            has_been_accepted = JobApplication.objects.get(applied_by = applicant, vacancy = instance).has_been_accepted
            response.append({'applicant_id': applicant_id,'applicant_name':applicant_name, 
                             'applicant_avatar':applicant_avatar, 'applicant_tagline':applicant_tagline,
                             'has_been_accepted':has_been_accepted})
        return response
    
    def get_applicant_avatar(self, instance):
        try:
            name = instance.applicant.avatar.url
            url  = self.context['request'].build_absolute_uri(name)
            return url
        except:
            return None
        
        
class JobCreateVacanySerializer(serializers.ModelSerializer):
    class Meta:
        model   = JobVacancy
        fields  = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    application_id = serializers.CharField(source = 'id')

    class Meta:
        model   = JobApplication
        fields  = ('application_id','has_been_accepted')
    
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['vacancy_id'] = instance.vacancy.id
        response['title'] = instance.vacancy.title
        response['organization'] = instance.vacancy.organization
        response['location'] = instance.vacancy.location
        response['is_remote'] = instance.vacancy.is_remote
        response['logo'] = self.get_logo(instance)
        return response
    
    def get_logo(self, instance):
        try:
            name = instance.vacancy.file_linked.url
            url  = self.context['request'].build_absolute_uri(name)
            return url
        except:
            return None
        
        
class JobApplicationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model   = JobApplication
        fields  = '__all__'