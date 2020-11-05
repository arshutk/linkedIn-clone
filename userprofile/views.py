from django.shortcuts import render

from userprofile.models import WorkExperience, Education

from userprofile.serializers import WorkExperienceSerializer, EducationSerializer

from rest_framework import views, generics, viewsets

from rest_framework.permissions import AllowAny


class WorkExperienceViewset(viewsets.ModelViewSet):
    
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer


class EducationViewset(viewsets.ModelViewSet):
    
    queryset = Education.objects.all()
    serializer_class = EducationSerializer