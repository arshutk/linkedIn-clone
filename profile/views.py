from django.shortcuts import render


from profile.models import  WorkExperience, Education, LicenseAndCertification, VolunteerExperience, Course, Project, TestScore, \
                            Skill, SocialProfile, ProfileView, JobVacancy, JobApplication

from profile.serializers import WorkExperienceSerializer, EducationSerializer, LicenseAndCertificationSerializer, \
                                VolunteerExperienceSerializer, CourseSerializer, ProjectSerializer, TestScoreSerializer, \
                                SkillSerializer, SkillCreateSerializer, EndorsementSerializer, SocialProfileSerializer, ProfileViewSerializer, JobCreateVacanySerializer, \
                                JobApplicationCreateSerializer, JobApplicationSerializer, JobVacanySerializer

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

from django.shortcuts import get_object_or_404

from rest_framework import filters

from random import choice

from notification.models import Notification


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
        social_profile   = get_object_or_404(UserProfile, id = profile_id).social_profile
        
        if update_tagline:   
            serializer = WorkExperienceSerializer(data = request.data, context = {'request':request})
            if serializer.is_valid():
                serializer.save()
                social_profile.tagline = f"{serializer.data['position']} at {serializer.data['organization_name']}"
                social_profile.save()
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
    
    def get(self, request, profile_id = None):
        user = get_object_or_404(UserProfile, id = profile_id)
        try:
            query = user.skills  
        except:
            raise Http404
        serializer = SkillSerializer(query, context = {'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, profile_id = None):
        data            = request.data.copy()
        skills          = request.data.get('skills_list')
        if profile_id:
            data['user']    = profile_id
            if skills:
                if len(skills) <= 3:
                    data['top_skills'] = json.dumps(skills)
                    data['skills_list'] = json.dumps(skills)
                    serializer = SkillCreateSerializer(data = data, context={'request': request})
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status = status.HTTP_201_CREATED)
                    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                data['top_skills'] = json.dumps(skills[:3])
                data['skills_list'] = json.dumps(skills)
                serializer = SkillCreateSerializer(data = data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'Skills list must not be empty.'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Provide id.'}, status = status.HTTP_400_BAD_REQUEST)
    
    
class SkillUpdateView(views.APIView):

    def put(self, request, skill_id):
        data            = request.data.copy()
        skills_list     = data.get('skills_list')
        
        skills = get_object_or_404(Skill, id = skill_id)
        
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
        skills = get_object_or_404(Skill, id = skill_id )
        skills_list = json.decoder.JSONDecoder().decode(skills.skills_list)
        
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


class SkillEndorsementView(views.APIView):
    
    def post(self, request, skill_id):
        user = request.user.profile
        data = request.data.copy()
        endorsed_skill = request.data.get('skill_name')
        
        skill = get_object_or_404(Skill, id = skill_id)   
        skills_list = json.decoder.JSONDecoder().decode(skill.skills_list)
        
        for endorsement in skill.endorsements.all():
            if endorsed_skill == endorsement.skill_name and user == endorsement.user:
                return Response({'detail':'Cannot endorse a skill twice.'}, status = status.HTTP_406_NOT_ACCEPTABLE)

        if endorsed_skill:
            if endorsed_skill in skills_list:
                data['skill'] = skill_id
                data['user'] = user.id
                serializer = EndorsementSerializer(data = data, context = {'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Can\'t endorse skill that has not yet been added.'}, status = status.HTTP_403_FORBIDDEN)
        return Response({'detail': 'Provide the skill that has to be endorsed.'}, status = status.HTTP_403_FORBIDDEN)


class GetWorkView(views.APIView):
    
    def get(self, request, profile_id = None):

        user = get_object_or_404(UserProfile, id = profile_id)
        
        try:
            work_experience = user.work_experience.all()
            serializer = WorkExperienceSerializer(work_experience, many = True, context = {'request':request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except:
            return Response({'detail':'No work experience yet'}, status = status.HTTP_400_BAD_REQUEST)
        
        
class GetAcademicView(views.APIView):
    
    def get(self, request, profile_id = None):
        user = get_object_or_404(UserProfile, id = profile_id)
        
        try:
            academic_experience = user.education.all()
            serializer = EducationSerializer(academic_experience, many = True, context = {'request':request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except:
            return Response({'detail':'No academic experience yet'}, status = status.HTTP_400_BAD_REQUEST)
             

class ProfileStrengthView(views.APIView):
    
    def get(self, request):
        user = get_object_or_404(UserProfile, id = request.user.profile.id)
        
        message             = dict()
        profile_strength    = 0
        
        avatar              = user.avatar
        article             = user.articles.count()
        connections         = user.request_received.filter(has_been_accepted = True).count() + \
                              user.request_sent.filter(has_been_accepted = True).count()
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
            
        # if len(message) == 0:
        #     return Response({'detail': 'User has completed his profile.'}, status = status.HTTP_204_NO_CONTENT)      
        return Response({'profile_strength': profile_strength, 'message': message}, status = status.HTTP_200_OK)
            
   
        
class DasboardView(views.APIView):   
    def get(self, request, profile_id = None):
        user = get_object_or_404(UserProfile, id = profile_id)
        
        profile_views       = user.social_profile.viewer_list.count()
        no_of_articles      = user.articles.count()
        bookmarked_posts    = user.bookmarked_posts.count()
        
        return Response({'profile_views':profile_views, 
                         'no_of_articles':no_of_articles, 
                         'bookmarked_posts':bookmarked_posts}, 
                          status = status.HTTP_200_OK)
        

class BannerView(views.APIView):
    
    def get(self, request, profile_id = None):
        user = get_object_or_404(UserProfile, id = profile_id)
        viewer = get_object_or_404(UserProfile, id = request.user.profile.id)

        if viewer != user:
            viewer = request.user.profile
            user.social_profile.viewer_list.add(viewer)
            connection_status = (Connection.objects.filter(sender = viewer, receiver = user) | \
                                 Connection.objects.filter(sender = user, receiver = viewer))
            if connection_status:
                if connection_status[0].has_been_accepted:
                    is_connected = True
                    is_pending = False
                    connection_id = connection_status[0].id
                else:
                    is_connected = False
                    is_pending = True
                    connection_id = connection_status[0].id
            else:
                is_connected = False
                is_pending = False
                connection_id = None
        else:
            is_connected = None
            is_pending = None
            connection_id = None
            
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
        
        return Response({'avatar':avatar,'first_name':first_name, 'last_name':last_name, 
                         'location':location,'tagline':tagline,'experience':experience, 
                         'connection':connection, 'profile_views':profile_views, 'bookmarked_posts':bookmarked_posts, 
                         'about':about,'is_connected':is_connected,'is_pending':is_pending,'connection_id':connection_id}, 
                          status = status.HTTP_200_OK)
        
        
class BannerUpdateView(views.APIView):
    
    def put(self, request, profile_id = None):
        
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
        
        try: 
            del data['bio']
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
        return Response(profile_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, profile_id = None): 
        bio = request.data.get('bio')
        social_profile = SocialProfile.objects.get(id = profile_id)
        serializer = SocialProfileSerializer(social_profile, data = {'bio':bio}, partial = True, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class JobVacancyView(viewsets.ViewSet):
    
    queryset    = JobVacancy.objects.all()    
    
    def get(self, request):
        user = request.user.profile   
        data = JobVacancy.objects.filter(posted_by = user)
        serializer = JobVacanySerializer(data, many = True,context = {'request': request, 'user': user})
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        vacancy = get_object_or_404(JobVacancy, id = pk)
        serializer = JobVacanySerializer(vacancy, context = {'request': request, 'user': request.user.profile })
        return Response(serializer.data, status = status.HTTP_200_OK)
     
    def create(self, request):
        data = request.data.copy()
        data['posted_by'] = request.user.profile.id
        serializer = JobCreateVacanySerializer(data = data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)       
    
    def partial_update(self, request, pk):
        vacancy = get_object_or_404(JobVacancy, id = pk)
        # if vacancy.is_closed:
        vacancy.viewed_by.clear() 
        vacancy.saved_by.clear() 
        vacancy.applicants.clear() 
        data = request.data.copy()
        try:
            del data['posted_by']
        except:
            pass
        try:
            del data['organization']
        except:
            pass
        user = request.user.profile
        if user == vacancy.posted_by:
            serializer = JobCreateVacanySerializer(vacancy, data = request.data, partial = True, context = {'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Cannot edit job vacancies of other users.'}, status = status.HTTP_403_FORBIDDEN)
        # return Response({'detail': 'First close the job vacancy to edit.'}, status = status.HTTP_403_FORBIDDEN)
        
    
    def destroy(self, request, pk):
        vacancy = get_object_or_404(JobVacancy, id = pk)
        vacancy.delete()
        return Response({'detail': 'Job vacancy removed successfully.'}, status = status.HTTP_204_NO_CONTENT)
    
class VacancyApplyView(views.APIView):
    def post(self, request, vacancy_id):
        vacancy = get_object_or_404(JobVacancy, id = vacancy_id)
        applicant = request.user.profile
        if not vacancy.posted_by == applicant.id:
            data = request.data.copy()
            applicant = request.user.profile
            data['applied_by'] = applicant.id
            data['vacancy'] = vacancy.id
            serializer = JobApplicationCreateSerializer(data = data, context = {'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'You can\'t apply on a vacancy of yours.'}, status = status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, vacancy_id):
        vacancy = get_object_or_404(JobVacancy, id = vacancy_id)
        applicant = request.user.profile
        try:
            vacancy.applicants.remove(applicant)
            return Response({'detail': 'Application deleted.'}, status = status.HTTP_204_NO_CONTENT)
        except:
            return Response({'detail': 'Already not applied.'}, status = status.HTTP_204_NO_CONTENT)

class AppliedVacancyGetView(views.APIView):
        def get(self, request, vacancy_id = None):
            user = request.user.profile
            applications = JobApplication.objects.filter(applied_by = user).all()
            serializer = JobApplicationSerializer(applications, many = True, context = {'request':request})
            return Response(serializer.data, status = status.HTTP_200_OK)
    

class VacancyReviewView(views.APIView):
        def patch(self, request, vacancy_id, applicant_id):
            application = JobApplication.objects.get(vacancy = vacancy_id, applied_by = applicant_id)
            user = request.user.profile
            choice = request.data['has_been_accepted']
            if application.vacancy.posted_by == user:
                if choice:
                    application.has_been_accepted = True
                    application.save()
                    target = UserProfile.objects.get(id = applicant_id)
                    Notification.objects.create(target = target, source = application.vacancy.posted_by, action = 'application_accepted', 
                    detail = f'Your application to {application.vacancy.organization} for postion of {application.vacancy.title} has been accepted.',
                    action_id = vacancy_id)
                    return Response({'detail':'Application accepted.'}, status = status.HTTP_202_ACCEPTED)
                elif choice == False:
                    if application.has_been_accepted:
                        try:
                            Notification.objects.get(target = applicant_id, source = application.vacancy.posted_by,
                                                 action = 'application_accepted', action_id = vacancy_id).delete()
                        except:
                            pass
                    application.has_been_accepted = False
                    application.save()
                    return Response({'detail':'Application rejected.'}, status = status.HTTP_204_NO_CONTENT)
                return Response({'detail':'Choice to accept/reject apllication not provided.'}, status = status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'Only employer can mark application.'}, status = status.HTTP_401_UNAUTHORIZED)
    

class VacancyBookmarkView(views.APIView):  
    def post(self, request, vacancy_id):
        vacancy = get_object_or_404(JobVacancy, id = vacancy_id)
        user = request.user.profile
        if user not in vacancy.saved_by.all():
            vacancy.saved_by.add(user)
            return Response({'detail': 'Vacancy saved.'}, status = status.HTTP_200_OK)
        return Response({'detail': 'Already saved.'}, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, vacancy_id):
        vacancy = get_object_or_404(JobVacancy, id = vacancy_id)
        user = request.user.profile
        if user in vacancy.saved_by.all():
            vacancy.saved_by.remove(user)
            return Response({'detail': 'Bookmark removed.'}, status = status.HTTP_200_OK)
        return Response({'detail': 'No bookmark to vacncy found.'}, status = status.HTTP_400_BAD_REQUEST)
    
class VacancyBookmarkGetView(views.APIView):
    def get(self, request):
        user = request.user.profile
        bookmarks = JobVacancy.objects.filter(saved_by = user)
        serializer = JobVacanySerializer(bookmarks, many = True, context = {'request': request, 'user':user})
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class VacancyRecommendView(views.APIView):
    def get(self, request):
        user = request.user.profile
        try:
            user_skills = json.decoder.JSONDecoder().decode(user.skills.skills_list)
        except:
            user_skills = None
        query = JobVacancy.objects.all()
        print(query)
        response = list()
        if user_skills:
            for vacancy in query:
                try:
                    for skill in vacancy.skills_required.split(','):
                        if skill.strip() in user_skills:
                            response.append(vacancy)
                            break
                except:
                    continue
            if len(response) < 5:
                try:
                    [response.append(query[count]) for count in range(7) if query[count] not in response]
                except:
                    pass
            serializer = JobVacanySerializer(response, many = True, context = {'request': request, 'user':user})
            return Response(serializer.data, status = status.HTTP_200_OK)
        query = choice(query)
        serializer = JobVacanySerializer(query, many = True, context = {'request': request, 'user':user})
        print(serializer.data)
        return Response(serializer.data, status = status.HTTP_200_OK)
                
        
# Search

class JobSearchView(generics.ListAPIView):
    queryset = JobVacancy.objects.all()
    serializer_class = JobVacanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['skills_required', 'employment_type','title' ,'industry', 'description']
    
    def get_serializer_context(self):
        # print(self.request.query_params.get('radius'))
        context = super(JobSearchView, self).get_serializer_context()
        context.update({"request": self.request, 'user': self.request.user.profile})
        return context
        





