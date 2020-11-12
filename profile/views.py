from django.shortcuts import render

from profile.models import  WorkExperience, Education, LicenseAndCertification, VolunteerExperience, Course, Project, TestScore, Skill
# , FeaturedSkill

from profile.serializers import WorkExperienceSerializer, EducationSerializer, LicenseAndCertificationSerializer, VolunteerExperienceSerializer, CourseSerializer, ProjectSerializer, TestScoreSerializer, SkillSerializer
# , FeaturedSkillSerializer

from rest_framework import views, generics, viewsets

from profile.permissions import IsAuthenticatedAndOwner

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import status

from rest_framework.response import Response

import json


class WorkExperienceViewset(viewsets.ModelViewSet):
    
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class EducationViewset(viewsets.ModelViewSet):
    
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
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
        skills          = request.data.get('skills')
        
        
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
    

    def partial_update(self, request, pk):
        
        top_skills = request.data.get('top_skills')
        
        skills = Skill.objects.get(pk = pk)
        
        
        if top_skills:
            if len(top_skills) <= 3:
                if len(top_skills) == 3:
                    serializer = SkillSerializer(skills, data = request.data, partial=True, context={'request': request})
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

    
#     {
#                  "skills": ["C++", "Python", "Java", "Public Speaking", "Writing","Django", "Collaborative Problem Solving"], 
#                  "top_skills": ["Python", "Java", "Public Speaking"], "user": "3"
# }