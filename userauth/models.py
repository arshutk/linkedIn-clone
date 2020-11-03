from django.db import models

from django.contrib.auth.models import (
        BaseUserManager, AbstractBaseUser
        )

import datetime

from django.conf import settings



class UserManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have an email password')

        user = self.model(
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff  = True
        user.admin  = True
        user.active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active      = models.BooleanField(default = False)
    staff       = models.BooleanField(default = False)
    admin       = models.BooleanField(default = False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):          
        return self.email

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class OTPModel(models.Model):
    
    otp              = models.CharField(max_length = 6)
    email_linked     = models.EmailField()
    phone_linked     = models.CharField(max_length = 10)
    time_created     = models.IntegerField()

    def __str__(self):
        return f"{self.email_linked} : {self.otp}"
    class Meta:
        verbose_name = 'OTP Model'
        verbose_name_plural = 'OTP Models'
    
class UserProfile(models.Model):

    user                = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name ='profile')
    first_name          = models.CharField(max_length = 30)
    last_name           = models.CharField(max_length = 30)
    avatar              = models.ImageField(upload_to = 'avatar/', blank = True, null = True, max_length = 1048576) #1MB
    location            = models.CharField(max_length = 50)
    phone_number        = models.CharField(max_length = 10, blank = True)
    
    is_employed         = models.BooleanField(default = False)
    organization_name   = models.CharField(max_length = 50)
    position            = models.CharField(max_length = 50)
    start_date          = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    end_date            = models.DateField(blank = True, null = True, default = None)
    is_online           = models.BooleanField(default = False)
    
    followers            = models.ManyToManyField('self', related_name ='follow', blank = True)
    
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class UserJobExperience(models.Model):
     
    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='job_experience')
    organization_name   = models.CharField(max_length = 50)
    position            = models.CharField(max_length = 50)
    start_date          = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    end_date            = models.DateField(blank = True, null = True, default = None)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.organization_name}'
    
    class Meta:
        verbose_name = 'User Job Experience'
        verbose_name_plural = 'User Job Experiences'
        
class UserStudyExperience(models.Model):
     
    user                = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='study_experience')
    organization_name   = models.CharField(max_length = 50)
    start_date          = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    end_date            = models.DateField(blank = True, null = True, default = None)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.organization_name}'
    
    class Meta:
        verbose_name = 'User Study Experience'
        verbose_name_plural = 'User Study Experiences'
     
# class Connection(models.Model):
#     # connections        = models.ManyToManyField(UserProfile, related_name ='connected_user', blank = True, through='Request') 
#     user               = models.OneToOneField(UserProfile, on_delete = models.CASCADE)
#     connections        = models.ManyToManyField(UserProfile, related_name ='connections', through = 'ConnectionRequest', blank = True) 
#     pending_request    = models.ManyToManyField(UserProfile, related_name ='pending_connection', through = 'PendingConnectionRequest', blank = True)
    
#     def __str__(self):
#         return f'{self.user.first_name} {self.user.last_name}'
    
#     class Meta:
#         verbose_name = 'Connection'
#         verbose_name_plural = 'Connections'
        
            

# class ConnectionRequest(models.Model): # Connection Intermdiate Model
#     user               = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
#     connections        = models.ForeignKey(Connection, on_delete = models.CASCADE)
#     date_time          = models.DateTimeField(auto_now_add = True)
    
#     def __str__(self):
#         return f'{self.user}'
    
#     class Meta:
#         unique_together = [['user','connections']]
#         verbose_name = 'Connected User'
#         verbose_name_plural = 'Connected Users'



# class PendingConnectionRequest(models.Model): # Pending Connection Intermdiate Model
#     user               = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
#     requests           = models.ForeignKey(Connection, on_delete = models.CASCADE)
#     date_time          = models.DateTimeField(auto_now_add = True)
    
#     def __str__(self):
#         return f'{self.user}'
    
#     class Meta:
#         unique_together = [['user','requests']]
#         verbose_name = 'Connection Request'
#         verbose_name_plural = 'Connection Requests'
   
class Connection(models.Model):
    
    receiver               = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = 'connections')
    sender                 = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = 'connection_request_sent')
    date_time              = models.DateTimeField(auto_now = True)
    has_been_accepted      = models.BooleanField(default = False)
    is_visible             = models.BooleanField(default = True)
    
    def __str__(self):
        return f'{self.sender.first_name} {self.sender.last_name} > {self.receiver.first_name} {self.receiver.last_name}'

           

