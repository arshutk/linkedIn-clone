from django.db import models

import datetime

from userauth.models import UserProfile



class Organization(models.Model):
    name                = models.CharField(max_length = 50)
    headquarter         = models.CharField(max_length = 50)
    website_url         = models.URLField(unique = True)
    
    def __str__(self):
        return f'{self.name} : {self.headquarter} : {self.website_url}'
    
    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
    
   
    
class OrganizationDetail(models.Model):
    INDUSTRY = (
                ('Accounting','Accounting'),
                ('Aviation','Aviation'),
                ('Animation','Animation'),
                ('Architecture','Architecture'),
                ('Arts and Craft','Arts and Craft'),
                ('Biotechnology','Biotechnology'),
                ('Civil Engineering','Civil Engineering'),
                ('Computer Network','Computer Network'),
                ('Computer Hardware','Computer Hardware'),
                ('Computer Software','Computer Software'),
                ('Education','Education'),
                ('Pharmaceutical','Pharmaceutical'),
               )
    SIZE = (
                ('10','1-10'),   
                ('50','10-50'),   
                ('100','50-100'),   
                ('500','100-500'),   
                ('1000','500-1000'),   
                ('5000','1000-5000'),   
                ('10000','5000-10000'),   
                ('10000','10000+'),   
               )
    TYPE = (
                ('Public','Public'),
                ('Government','Government'),
                ('Private','Private'),
                ('Nonprofit','Nonprofit'),
               )
    
    oganization            = models.OneToOneField(Organization, on_delete = models.CASCADE, related_name ='detail')
    organization_industry  = models.CharField(choices = INDUSTRY, default = None, max_length = 50)
    organization_size      = models.CharField(choices = SIZE, default = None, max_length = 50)
    organization_type      = models.CharField(choices = TYPE, default = None, max_length = 50)
    
    
    def __str__(self):
        return f'{self.organisation.name} : {self.organization_size}'
    
    class Meta:
        verbose_name = 'Organization Detail'
        verbose_name_plural = 'Organization Details'
    


class OrganizationProfile(models.Model):
    oganization         = models.OneToOneField(Organization, on_delete = models.CASCADE, related_name ='profile')
    description         = models.TextField()
    tagline             = models.CharField(max_length = 20)
    logo                = models.ImageField(upload_to = 'organization/logo', blank = True, null = True, max_length = 1048576) #1MB
    
    def __str__(self):
        return f'{self.organisation.name} : {self.tagline}'
    
    class Meta:
        verbose_name = 'Organization Profile'
        verbose_name_plural = 'Organization Profiles'
    
    
    
class OrganizationStaff(models.Model):
    oganization         = models.OneToOneField(Organization, on_delete = models.CASCADE, related_name ='staff')
    page_superadmin     = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='superadmin_of_pages')
    page_admins         = models.ManyToManyField(UserProfile, blank = True, related_name ='admin_of_pages')
    employees           = models.ForeignKey(UserProfile, on_delete = models.CASCADE, blank = True, null = True)
    
    def __str__(self):
        return f'{self.organisation.name} : {self.page_superadmin.first_name} {self.page_superadmin.last_name}'
    
    class Meta:
        verbose_name = 'Organization Staff'
        verbose_name_plural = 'Organization Staff'
 
 
    
class OrganizationAnalytic(models.Model):
    oganization         = models.OneToOneField(Organization, on_delete = models.CASCADE, related_name ='viewed_by')
    viewed_by           = models.ManyToManyField(UserProfile, blank = True)
    
    
    def __str__(self):
        return f'{self.organisation.name}'
    
    class Meta:
        verbose_name = 'Organization Analytic'
        verbose_name_plural = 'Organization Analytics'


    
# class JobVacancy(models.Model):
#     TYPE = (
#                 ('Fulltime','Full-Time'),
#                 ('Parttime','Part-Time'),
#                 ('Internship','Internship'),
#                 ('Contract','Contract'),
#                )
    
#     oganization         = models.ForeignKey(Organization, on_delete = models.CASCADE, related_name ='vacancies')
#     title               = models.CharField(max_length = 30)
#     is_remote           = models.BooleanField(default = False)
#     location            = models.CharField(max_length = 50)
#     employement_type    = models.CharField(choices = TYPE, default = None, max_length = 50)
#     description         = models.TextField()
#     file_linked         = models.FileField(upload_to='organisation/jobs', null = True, blank = True, max_length = 1048576)
#     skills_required     = models.CharField(max_length = 30)
    
    
#     def __str__(self):
#         return f'{self.organisation.name} : {self.title} : {self.location}'
    
#     class Meta:
#         verbose_name = 'Job Vacancy'
#         verbose_name_plural = 'Job Vacancies'

# class JobVacancyQuestion(models.Model):
#     organization        = models.ForeignKey(JobVacancy, on_delete = models.CASCADE, related_name = 'screening_questions')
#     pass
    
    
    
    
    
