from django.shortcuts import render

from profile.models import  WorkExperience, Education, LicenseAndCertification, VolunteerExperience, Course, Project, TestScore, \
                            Skill, SocialProfile

from profile.serializers import WorkExperienceSerializer, EducationSerializer, LicenseAndCertificationSerializer, \
                                VolunteerExperienceSerializer, CourseSerializer, ProjectSerializer, TestScoreSerializer, \
                                SkillSerializer, SocialProfileSerializer

from rest_framework import views, generics, viewsets

from profile.permissions import IsAuthenticatedAndOwner

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import status

from rest_framework.response import Response

import json

from userauth.models import UserProfile

from django.http import Http404

from network.models import Connection


class SocialProfileView(viewsets.ModelViewSet):
    
    queryset = SocialProfile.objects.all()
    serializer_class = SocialProfileSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = []
        return [permission() for permission in permission_classes]

class WorkExperienceViewset(viewsets.ModelViewSet):
    
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = []
            # permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = []
        return [permission() for permission in permission_classes]


class EducationViewset(viewsets.ModelViewSet):
    
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [IsAuthenticatedAndOwner]
            permission_classes = []
        elif self.action == 'list':
            permission_classes = []
        return [permission() for permission in permission_classes]


class LicenseAndCertificationViewset(viewsets.ModelViewSet):
    
    queryset = LicenseAndCertification.objects.all()
    serializer_class = LicenseAndCertificationSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    
class VolunteerExperienceViewset(viewsets.ModelViewSet):
    
    queryset = VolunteerExperience.objects.all()
    serializer_class = VolunteerExperienceSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]



class CourseViewset(viewsets.ModelViewSet):
    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    
    
class ProjectViewset(viewsets.ModelViewSet):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    
class TestScoreViewset(viewsets.ModelViewSet):
    
    queryset = TestScore.objects.all()
    serializer_class = TestScoreSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    


class SkillsViewset(viewsets.ModelViewSet):
    
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    
    def create(self, request):
        data            = request.data.copy()
        skills          = request.data.get('skills_list')
        
        
        if skills:
            if len(skills) <= 3:
                data['top_skills'] = json.dumps(skills)
                serializer = SkillSerializer(data = data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            data['top_skills'] = json.dumps(skills[:3])
            serializer = SkillSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Skills list must not be empty.'}, status = status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        data            = request.data.copy()
        skills_list     = data.get('skills_list')
        
        skills          = Skill.objects.get(pk = pk)
        
        
        if skills:
            if len(skills_list) <= 3:
                data['top_skills'] = json.dumps(skills_list)
                serializer = SkillSerializer(skills, data = data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            data['top_skills'] = json.dumps(skills_list[:3])
            serializer = SkillSerializer(skills, data = data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Skills list must not be empty.'}, status = status.HTTP_400_BAD_REQUEST)
    
    
    def partial_update(self, request, pk):
        
        top_skills = request.data.get('top_skills')
        
        skills = Skill.objects.get(pk = pk)
        
        
        if top_skills:
            if len(top_skills) <= 3:
                if len(top_skills) == 3:
                    top_skills = json.dumps(top_skills)
                    serializer = SkillSerializer(skills, data = {'top_skills':top_skills}, partial=True, context={'request': request})
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status = status.HTTP_200_OK)
                    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                for skill in json.decoder.JSONDecoder().decode(skills.top_skills):
                    if skill in top_skills:
                        continue
                    top_skills.append(skill)
                    if len(top_skills) == 3:
                        top_skills = json.dumps(top_skills)
                        break         
                serializer = SkillSerializer(skills, data = {'top_skills': top_skills}, partial = True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'Please select only top three skills to feature.'}, status = status.HTTP_400_BAD_REQUEST)   
        return Response({'detail':'Featured Skills list has not been changed.'}, status = status.HTTP_304_NOT_MODIFIED)   
                
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes] 

    

#  {
#                  "top_skills": ["Django", "Java"]

# }

class GetWorkView(views.APIView):
    
    def get(self, request):
        
        user = request.user.profile 
        
        try:
            work_experience = user.work_experience.all()
            serializer = WorkExperienceSerializer(work_experience, many = True, context = {'request':request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except:
            return Response({'detail':'No work experience yet'}, status = status.HTTP_200_OK)
        
        
class GetAcademicView(views.APIView):
    
    def get(self, request):
        
        user = request.user.profile 
        
        try:
            academic_experience = user.education.all()
            serializer = EducationSerializer(academic_experience, many = True, context = {'request':request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except:
            return Response({'detail':'No work experience yet'}, status = status.HTTP_200_OK)
             

class ProfileStrengthView(views.APIView):
    
    def get_user(self, profile_id):
        try:
            return UserProfile.objects.get(id = profile_id)
        except:
            raise Http404
    
    def get(self, request):
        user                = self.get_user(request.user.profile.id)
        
        message             = dict()
        profile_strength    = 0
        
        avatar              = user.avatar
        article             = user.articles.count()
        connections         = user.connection_request_received.filter(has_been_accepted = True).count() + \
                              user.connection_request_sent.filter(has_been_accepted = True).count()
        try:
            skills          = len(user.skills.skills_list)
        except:
            skills          = 0
            
        work_experiences    = user.work_experience.count()
        academics           = user.education.count()
        bio                 = user.social_profile.bio
        
        
        if avatar:
            profile_strength += 1
            message['Profile Picture'] = True
        else:
            message['Profile Picture'] = False        

        if article:
            profile_strength += 1
            message['Article(1+)'] = True
        else:
            message['Article(1+)'] = False  
        
        if connections > 20:
            profile_strength += 1
            message['Connections(20+)'] = True
        else:
            message['Connections(20+)'] = False        

        if skills >= 5:
            profile_strength += 1
            message['Skills(5+)'] = True
        else:
            message['Skills(5+)'] = False        

        if work_experiences:
            profile_strength += 1
            message['Work Experience'] = True 
        else:
            message['Work Experience'] = False        

        if academics:
            profile_strength += 1
            message['Academics'] = True
        else:
            message['Academics'] = False        

        if bio:
            profile_strength += 1
            message['About'] = True
        else:
            message['About'] = False        

        if len(message) == 0:
            return Response({'detail': 'User has completed his profile.'}, status = status.HTTP_204_NO_CONTENT)      
        return Response({'profile_strength': profile_strength, 'message': message}, status = status.HTTP_200_OK)
            
   
        
class DasboardView(views.APIView):  
        
    def get(self, request):
        user                = request.user.profile
        
        profile_views       = 0
        no_of_articles      = user.articles.count()
        bookmarked_posts    = user.bookmarked_posts.count()
        
        return Response({'profile_views':profile_views, 
                         'no_of_articles':no_of_articles, 
                         'bookmarked_posts':bookmarked_posts}, 
                          status = status.HTTP_200_OK)
        

class BasicInfoView(views.APIView):
    
    def get(self, request):
        user                = request.user.profile
        data                = dict()
        try:
            domain_name = request.META['HTTP_HOST']
            picture_url = user.avatar.url
            absolute_url = 'http://' + domain_name + picture_url
            avatar = absolute_url
        except:
            avatar = None
            
        first_name          = user.first_name
        last_name           = user.last_name 
        headline            = user.social_profile.headline.split()
        position            = f'{headline[0]} {headline[1]}' 
        organization        = headline[2]       
        connection          = Connection.objects.filter(sender = user, has_been_accepted = True).count() + \
                              Connection.objects.filter(receiver = user, has_been_accepted = True).count()
        profile_views       = 0
        bookmarked_posts    = user.bookmarked_posts.count()
        
        work_experience     = user.social_profile.current_work_organization
        academic_experience = user.social_profile.current_academic_organization
        
        
        if work_experience:
            if academic_experience:
                experience  = [work_experience.organization_name, academic_experience.organization_name]
            else:
                experience  = [work_experience.organization_name]
        else:
            experience  = [academic_experience.organization_name]

            
        return Response({'avatar':avatar,
                         'first_name':first_name, 
                         'last_name':last_name, 
                         'position':position, 
                         'organization':organization, 
                         'organization':organization, 
                         'experience':experience, 
                         'connection':connection, 
                         'profile_views':profile_views, 
                         'bookmarked_posts':bookmarked_posts}, 
                          status = status.HTTP_200_OK)
        
        
        