from django.shortcuts import render


from profile.models import  WorkExperience, Education, LicenseAndCertification, VolunteerExperience, Course, Project, TestScore, \
                            Skill, SocialProfile, ProfileView

from profile.serializers import WorkExperienceSerializer, EducationSerializer, LicenseAndCertificationSerializer, \
                                VolunteerExperienceSerializer, CourseSerializer, ProjectSerializer, TestScoreSerializer, \
                                SkillSerializer, SocialProfileSerializer, ProfileViewSerializer

from rest_framework import views, generics, viewsets

from profile.permissions import IsAuthenticatedAndOwner

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import status

from rest_framework.response import Response

import json

from userauth.models import UserProfile

from userauth.serializers import UserProfileSerializer

from django.http import Http404

from network.models import Connection

from django.contrib.contenttypes.models import ContentType


class SocialProfileView(views.APIView):

    def get(self, request):
        
        queryset = SocialProfile.objects.all()
        serialzer = SocialProfileSerializer(queryset, many = True, context = {'request':request})
        return Response(serialzer.data, status = status.HTTP_200_OK)
        

class WorkExperienceViewset(viewsets.ViewSet):
    
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    
    def create(self, request):
        
        profile_id       = request.data.get('user')
        update_tagline   = request.data.get('update_tagline')
        
        social_profile   = UserProfile.objects.get(id = profile_id).social_profile
        
        if update_tagline:   
            serializer = WorkExperienceSerializer(data = request.data, context = {'request':request})
            if serializer.is_valid():
                serializer.save()
                print(social_profile.tagline)
                social_profile.tagline = f"{serializer.data['position']} at {serializer.data['organization_name']}"
                print(social_profile.tagline)
                social_profile.save()
                print(social_profile.tagline)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        serializer = WorkExperienceSerializer(data = request.data, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        
        instance       = WorkExperience.objects.get('pk')
        social_profile = request.data.user.social_profile
        update_tagline = request.data.get('update_tagline')
        
        if update_tagline:   
            serializer = WorkExperienceSerializer(instance, data = request.data, context = {'request':request})
            if serializer.is_valid():
                serializer.save()
                social_profile.tagline = f"{serializer.data['position']} at {serializer.data['organization_name']}"
                social_profile.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        serializer = WorkExperienceSerializer(instance, data = request.data, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    
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
    

class SkillView(views.APIView):
    
    def get(self, request):
        try:
            request.user.profile.skills
        except:
            raise Http404
        
        user  = request.user.profile
        query = user.skills  
        serializer = SkillSerializer(query, context = {'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)
    
        
    def post(self, request):
        data            = request.data.copy()
        skills          = request.data.get('skills_list')
        
        if skills:
            if len(skills) <= 3:
                data['top_skills'] = json.dumps(skills)
                data['skills_list'] = json.dumps(skills)
                serializer = SkillSerializer(data = data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            data['top_skills'] = json.dumps(skills[:3])
            data['skills_list'] = json.dumps(skills)
            serializer = SkillSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Skills list must not be empty.'}, status = status.HTTP_400_BAD_REQUEST)

class SkillUpdateView(views.APIView):

    def put(self, request, skill_id):
        
        data            = request.data.copy()
        skills_list     = data.get('skills_list')
        
        try:
            skills          = Skill.objects.get(pk = skill_id)
        except:
            raise Http404
        
        if skills:
            if len(skills_list) <= 3:
                data['top_skills'] = json.dumps(skills_list)
                data['skills_list'] = json.dumps(skills_list)
                serializer = SkillSerializer(skills, data = data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            data['top_skills'] = json.dumps(skills_list[:3])
            data['skills_list'] = json.dumps(skills_list)
            serializer = SkillSerializer(skills, data = data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Skills list must not be empty.'}, status = status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, skill_id):
        
        top_skills = request.data.get('top_skills')
        
        try:
            skills = Skill.objects.get(id = skill_id)
        except:
            raise Http404
        
        skills_list = json.decoder.JSONDecoder().decode(skills.skills_list)
        print(skills_list)
        
        if set(top_skills).issubset(set(skills_list)):
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
        return Response({'detail':'Some skill/s in featured list is/are not in added skill.'}, status = status.HTTP_304_NOT_MODIFIED)
    
    
    def delete(self, request, skill_id):
        Skill.objects.get(id = skill_id).delete()
        return Response({'detail':'Deleted'}, status = status.HTTP_204_NO_CONTENT)


class GetWorkView(views.APIView):
    
    def get(self, request):
        
        user = request.user.profile 
        
        try:
            work_experience = user.work_experience.all()
            serializer = WorkExperienceSerializer(work_experience, many = True, context = {'request':request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except:
            return Response({'detail':'No work experience yet'}, status = status.HTTP_400_BAD_REQUEST)
        
        
class GetAcademicView(views.APIView):
    
    def get(self, request):
        
        user = request.user.profile 
        
        try:
            academic_experience = user.education.all()
            serializer = EducationSerializer(academic_experience, many = True, context = {'request':request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except:
            return Response({'detail':'No academic experience yet'}, status = status.HTTP_400_BAD_REQUEST)
             

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
        

class BannerView(views.APIView):
    
    def get(self, request, profile_id):
        user    = UserProfile.objects.get(pk = profile_id)

        if request.user.profile != user:
            viewer = request.user.profile
            user.social_profile.viewer_list.add(viewer)
            
        try:
            domain_name = request.META['HTTP_HOST']
            picture_url = user.avatar.url
            absolute_url = 'http://' + domain_name + picture_url
            avatar = absolute_url
        except:
            avatar = None
            
        first_name          = user.first_name
        last_name           = user.last_name 
        location            = user.location
        tagline             = user.social_profile.tagline
        connection          = Connection.objects.filter(sender = user, has_been_accepted = True).count() + \
                              Connection.objects.filter(receiver = user, has_been_accepted = True).count()
        profile_views       = 0
        bookmarked_posts    = user.bookmarked_posts.count()
        
        try:
            work_experience     = user.social_profile.current_industry
        except:
            work_experience     = None
        
        try:
            academic_experience = user.social_profile.current_academia
        except:
            academic_experience = None
        
        if work_experience:
            if academic_experience:
                experience  = [work_experience.organization_name, academic_experience.organization_name]
            experience  = [work_experience.organization_name]
        else:
            if academic_experience:
                experience      = [academic_experience.organization_name]
            else:
                experience      = []

        about               = user.social_profile.bio
        
        return Response({'avatar':avatar,
                         'first_name':first_name, 
                         'last_name':last_name, 
                         'location':location,
                         'tagline':tagline, 
                         'experience':experience, 
                         'connection':connection, 
                         'profile_views':profile_views, 
                         'bookmarked_posts':bookmarked_posts, 
                         'about':about}, 
                          status = status.HTTP_200_OK)
        
        
class UserProfileUpdate(views.APIView):
    
    def patch(self, request, profile_id):
        
        user = UserProfile.objects.get(id = profile_id)
        
        data = request.data.copy()
        
        try: 
            del data['phone_number']
        except:
            pass
        
        serializer = UserProfileSerializer(user, data = data, partial = True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
     
        
class SocialProfileUpdate(views.APIView):
    
    def patch(self, request, profile_id):
        
        social_profile = UserProfile.objects.get(id = profile_id).social_profile
        
        data = request.data.copy()
        
        try: 
            del data['current_industry']
        except:
            pass
        
        try: 
            del data['current_academia']
        except:
            pass
        
        serializer = SocialProfileSerializer(social_profile, data = data, partial = True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
   
   
    
class BannerUpdateView(views.APIView):
    
    def put(self, request, profile_id):
        
        user    = UserProfile.objects.get(id = profile_id)       
        data    = request.data.copy()
        
        try: 
            del data['current_industry']
        except:
            pass
        
        try: 
            del data['current_academia']
        except:
            pass
        
        try: 
            del data['phone_number']
        except:
            pass
        
        profile_serializer = UserProfileSerializer(user, data = data, partial = True, context={'request': request})
        if profile_serializer.is_valid():
            profile_serializer.save()
            banner_serializer = SocialProfileSerializer(user.social_profile, data = data, partial = True, context={'request': request})
            if banner_serializer.is_valid():
                banner_serializer.save()
                data = {**profile_serializer.data, **banner_serializer.data}
                return Response(data, status = status.HTTP_202_ACCEPTED)
            return Response(banner_serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ProfieTrafficView(views.APIView):
    
    def get(self, request):
        data = list()
        social_profile = request.user.profile.social_profile
        views = social_profile.views.all()
        for view in views:
            # if view.viewer.social_profile.
            viewer_info = dict()
            viewer_info['avatar']       = view.viewer.avatar
            viewer_info['name']         = f'{view.viewer.first_name} {view.viewer.last_name}'
            viewer_info['tagline']      = view.viewer.social_profile.tagline
            viewer_info['time_elapsed'] = view.viewed_time
            passs

                


