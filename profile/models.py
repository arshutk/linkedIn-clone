from django.db import models

from userauth.models import UserProfile

import datetime

from organization.models import Organization 

from django.db.models import F

# - => Descending

# Background
class WorkExperience(models.Model):
     
    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='work_experience')
    organization_name   = models.CharField(max_length = 50)
    position            = models.CharField(max_length = 50)
    start_date          = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    end_date            = models.DateField(blank = True, null = True, default = None)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.organization_name}'
    
    class Meta:
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experiences'
        ordering = ('end_date','start_date', '-id') # 2019 < 2020

class Education(models.Model):
     
    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='education')
    organization_name   = models.CharField(max_length = 50)
    start_date          = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    end_date            = models.DateField(blank = True, null = True, default = None)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.organization_name}'
    
    class Meta:
        verbose_name = 'Academic '
        verbose_name_plural = 'Academics'
        ordering = ('-start_date',)
        
        
class LicenseAndCertification(models.Model):
     
    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='certifications')
    certification_name  = models.CharField(max_length = 50)
    organization_name   = models.CharField(max_length = 50)
    issue_date          = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    expiration_date     = models.DateField(blank = True, null = True, default = None)
    credential_id       = models.TextField(max_length = 30, blank = True, null = True)
    credential_url      = models.URLField(blank = True, null = True)
    
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.certification_name}'
    
    class Meta:
        verbose_name = 'License And Certification'
        verbose_name_plural = 'License And Certifications'
        ordering = ('-issue_date',)
        
        
class VolunteerExperience(models.Model):
    ROLE = (
                ('Animal Welfare','Animal Welfare'),
                ('Arts and Culture','Arts and Culture'),
                ('Children','Children'),
                ('Civil Rights and Social Action','Civil Rights and Social Action'),
                ('Economic Empowerment','Economic Empowerment'),
                ('Education','Education'),
                ('Environment','Environment'),
                ('Health','Health'),
                ('Human Rights','Human Rights'),
                ('Politics','Politics'),
                ('Poverty Alleviation','Poverty Alleviation'),
                ('Veteran Support','Veteran Support'),
                ('Social Services','Social Services'),
                ('Science and Technology','Science and Technology'),
               )
     
    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='volunteer_experience')
    organization_name   = models.CharField(max_length = 50)
    role                = models.CharField(max_length = 50)
    cause               = models.CharField(choices = ROLE, default = None, max_length = 50)
    start_date          = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    end_date            = models.DateField(blank = True, null = True, default = None)
    description         = models.TextField(blank = True, null = True)

    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.organization_name}'
    
    class Meta:
        verbose_name = 'Volunteer Experience'
        verbose_name_plural = 'Volunteer Experiences'
        ordering = ('-start_date',)


# Accomplishments

class Course(models.Model):
     
    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='course_taken')
    course_name         = models.CharField(max_length = 50)
    passed_date         = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    organization_name   = models.CharField(max_length = 50)

    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.course_name}'
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ('-passed_date',)
        

class Project(models.Model):
     
    user                = models.ManyToManyField(UserProfile, blank = True, related_name ='project')
    project_name        = models.CharField(max_length = 50)
    start_date          = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    end_date            = models.DateField(blank = True, null = True, default = None)
    organization_name   = models.ForeignKey(Organization, on_delete = models.CASCADE, null = True, blank= True, related_name ='project_organization')
    project_url         = models.URLField(blank = True, null = True)
    description         = models.TextField()


    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.project_name}'
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ('-start_date',)
        
class TestScore(models.Model):
     
    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='test')
    title               = models.CharField(max_length = 50)
    test_date           = models.DateField(blank = True, null = True, default = None)
    organization_name   = models.ForeignKey(Organization, on_delete = models.CASCADE, null = True, blank= True, related_name ='test_organization')
    project_url         = models.URLField(blank = True, null = True)
    description         = models.TextField(blank = True, null = True)


    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.organization_name}'
    
    class Meta:
        verbose_name = 'Test Score'
        verbose_name_plural = 'Test Scores'
        ordering = ('-test_date',)
    
    
        
# Skills      
 
class Skill(models.Model):

    user                = models.OneToOneField(UserProfile, on_delete = models.CASCADE, related_name ='skills')
    skills_list         = models.TextField()
    top_skills          = models.TextField(blank = True, null = True)
    endorsed_by         = models.ManyToManyField(UserProfile, through = 'Endorsement')
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.top_skills}'
        
    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        
class Endorsement(models.Model):
    skill               = models.ForeignKey(Skill, on_delete = models.CASCADE, related_name = "endorsements")
    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "endorsed_skills")
    skill_name          = models.CharField(max_length = 50)
 

# Social Profile
    
class SocialProfile(models.Model):
    user                 = models.OneToOneField(UserProfile, on_delete = models.CASCADE, related_name ='social_profile')
    
    bio                  = models.TextField(blank = True, null = True)
    tagline              = models.CharField(max_length = 60, blank = True, null = True)
    background_photo     = models.ImageField(upload_to = 'background/', blank = True, null = True, max_length = 1048576)
    dob                  = models.DateField(blank = True, null = True, default = None)
    profile_url          = models.TextField(blank = True, null = True)
    
    current_industry     = models.OneToOneField(WorkExperience, blank = True, null = True, on_delete = models.SET_NULL, default = None, related_name ='current_work')
    current_academia     = models.OneToOneField(Education, blank = True, null = True,on_delete = models.SET_NULL, default = None, related_name ='current_academic')
    
    viewer_list          = models.ManyToManyField(UserProfile, through = 'ProfileView')
    
    is_private           = models.BooleanField(default = False)
    completely_private   = models.BooleanField(default = False) 
    semi_private         = models.BooleanField(default = False) 
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} > {self.tagline}'
    
    class Meta:
        verbose_name = 'Social Profile'
        verbose_name_plural = 'Social Profiles'
        
        
class ProfileView(models.Model):
    viewer          = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='viewed')
    profile         = models.ForeignKey(SocialProfile, on_delete = models.CASCADE, related_name ='views')
    viewed_time     = models.DateTimeField(auto_now_add = True)
        
    def __str__(self):
        return f'{self.viewer.first_name} {self.viewer.last_name} > {self.profile.user.first_name} {self.profile.user.last_name}'
    
    class Meta:
        verbose_name = 'Profile View'
        verbose_name_plural = 'Profile Views'
        # ordering = ('-date_viewed','user')
        
    
class JobVacancy(models.Model):
    TYPE = (
                ('Fulltime','Full-Time'),
                ('Parttime','Part-Time'),
                ('Internship','Internship'),
                ('Contract','Contract'),
                ('Volunteer','Volunteer'),
                ('Temporary','Temporary'),
               )
    
    # oganization         = models.ForeignKey(Organization, on_delete = models.CASCADE, related_name ='vacancies')
    organization        = models.CharField(max_length = 50)
    title               = models.CharField(max_length = 30)
    is_remote           = models.BooleanField(default = False, blank = True)
    location            = models.CharField(max_length = 50)
    employment_type     = models.CharField(choices = TYPE, max_length = 50)
    description         = models.TextField(blank = True)
    file_linked         = models.FileField(upload_to='user/jobs', null = True, blank = True, max_length = 1048576)
    skills_required     = models.CharField(max_length = 100, null = True, blank = True)  
    posted_by           = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='jobs_posted')
    industry            = models.CharField(max_length = 60)
    pay_range           = models.CharField(max_length = 60, null = True, blank = True)
    
    posted_at           = models.DateField(auto_now_add = True)
    
    is_closed           = models.BooleanField(default = False)
    show_profile        = models.BooleanField(default = True)
    
    external_site_url   = models.URLField(blank = True, null = True)
    
    saved_by            = models.ManyToManyField(UserProfile, related_name = "saved_jobs", blank = True)
    
    viewed_by           = models.ManyToManyField(UserProfile, blank = True)
    
    applicants          = models.ManyToManyField(UserProfile, through = 'JobApplication', related_name = 'jobs_applied_to')
    
    def __str__(self):
        return f'{self.organization} : {self.title} : {self.location}'
    
    class Meta:
        verbose_name = 'Job Vacancy'
        verbose_name_plural = 'Job Vacancies'
        
class JobApplication(models.Model):
    applied_by  = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    vacancy     = models.ForeignKey(JobVacancy, on_delete = models.CASCADE)
    time        = models.DateField(auto_now_add = True)
    remarks     = models.CharField(max_length = 100, null = True, blank = True)
    file_linked = models.FileField(upload_to='user/jobs', null = True, blank = True, max_length = 1048576)
    has_been_accepted = models.BooleanField(blank = True, null = True)
    
    def __str__(self):
        return f'{self.applied_by.first_name} {self.applied_by.last_name}'
    
    class Meta:
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        unique_together = ('applied_by', 'vacancy')
    



    