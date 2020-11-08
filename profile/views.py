from django.shortcuts import render

from profile import models 

from profile.serializers import WorkExperienceSerializer, EducationSerializer, LicenseAndCertificationSerializer, VolunteerExperienceSerializer, CourseSerializer, ProjectSerializer, TestScoreSerializer, SkillsSerializer

from rest_framework import views, generics, viewsets



class WorkExperienceViewset(viewsets.ModelViewSet):
    
    queryset = models.WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer


class EducationViewset(viewsets.ModelViewSet):
    
    queryset = models.Education.objects.all()
    serializer_class = EducationSerializer


class LicenseAndCertificationViewset(viewsets.ModelViewSet):
    
    queryset = models.LicenseAndCertification.objects.all()
    serializer_class = LicenseAndCertificationSerializer
    
    
class VolunteerExperienceViewset(viewsets.ModelViewSet):
    
    queryset = models.VolunteerExperience.objects.all()
    serializer_class = VolunteerExperienceSerializer



class CourseViewset(viewsets.ModelViewSet):
    
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    
    
    
class ProjectViewset(viewsets.ModelViewSet):
    
    queryset = models.Project.objects.all()
    serializer_class = ProjectSerializer
    
    
class TestScoreViewset(viewsets.ModelViewSet):
    
    queryset = models.TestScore.objects.all()
    serializer_class = TestScoreSerializer
    
  

class SkillsViewset(viewsets.ModelViewSet):
    
    queryset = models.Skills.objects.all()
    serializer_class = SkillsSerializer
    # <QueryDict: {'csrfmiddlewaretoken': ['rhW8nshISFS1NnS6CSPiLC1G3Z2j9BSgrKMygr8YrWy2O2THKVukDix0One7J6iE'], 
    # 'my_field': ['item_key2', 'item_key3', 'item_key4'], 'user': ['1']}>