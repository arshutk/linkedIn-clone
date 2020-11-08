from django.db import models

from userauth.models import UserProfile

import datetime

from organization.models import Organization 



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
        
        
class TestScore(models.Model):
     
    # user                = models.ManyToManyField(UserProfile, blank = True, related_name ='project')
    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='test')
    title               = models.CharField(max_length = 50)
    start_date          = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    end_date            = models.DateField(blank = True, null = True, default = None)
    organization_name   = models.ForeignKey(Organization, on_delete = models.CASCADE, null = True, blank= True, related_name ='test_organization')
    project_url         = models.URLField(blank = True, null = True)
    description         = models.TextField(blank = True, null = True)


    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.organization_name}'
    
    class Meta:
        verbose_name = 'Test Score'
        verbose_name_plural = 'Test Scores'
    
    
        
# Skills

from multiselectfield import MultiSelectField

SKILLS = (    ('Tools & Technology', (('C++', 'C++'), ('Python', 'Python'), ('Django', 'Django'), 
                             ('Java', 'Java'), ('Flutter', 'Flutter'), ('React', 'React'),
                             ('Android Development', 'Android Development'), ('Angular', 'Angular'), ('Flask', 'Flask'),
                             ('HTML', 'HTML'), ('CSS', 'CSS'), ('SASS', 'SASS'),
                             ('Bootstrap', 'Bootstrap'), ('Ruby', 'Ruby'), ('C#', 'C#'),
                             ('Spring', 'Spring'), ('Laraval', 'Laraval'), ('PHP', 'PHP'),
                             ('Node', 'Node'), ('Git', 'Git'), ('GitHub', 'GitHub'),
                             ('ASP.NET', 'ASP.NET'), ('Machine Learning', 'Machine Learning'), ('Big Data', 'Big Data'),
                             )),
          
              ('Interpersonal', (('Leadership', 'Leadership'), ('Team Management', 'Team Management'), ('Resource Management', 'Resource Management'),
                                 ('Team Building', 'Team Building'), ('Teamwork', 'Teamwork'), ('Public Speaking', 'Public Speaking'),
                                 ('Communication', 'Communication'), ('Writing', 'Writing'), ('Collaborative Problem Solving', 'Collaborative Problem Solving'),
                                 ('Strategic Negotiations', 'Strategic Negotiations'), ('Customer Service', 'Customer Service'),
                                )),
)
          
class Skills(models.Model):

    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='skills')
    skills              = MultiSelectField(choices = SKILLS)
    top_skills          = MultiSelectField(choices = SKILLS)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.skills}'
        
    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'