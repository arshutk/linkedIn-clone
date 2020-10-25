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
        user.staff = True
        user.admin = True
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


    
class UserProfile(models.Model):

    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name ='profile')
    first_name      = models.CharField(max_length = 30)
    last_name       = models.CharField(max_length = 30)
    avatar          = models.ImageField(upload_to = 'avatar/', blank = True, null = True, max_length = 1048576) #1MB
    location        = models.CharField(max_length = 50)
    phone_number    = models.CharField(max_length = 10, blank = True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class UserExperience(models.Model):
     
    user            = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name ='experience')
    name            = models.CharField(max_length = 50)
    is_employed     = models.BooleanField()
    position        = models.CharField(max_length = 50)
    start_year      = models.DateField(default = datetime.date.today) # yyyy-mm-dd
    end_year        = models.DateField()
    
    def __str__(self):
        return f'{self.name} -> {self.position}'
    
    class Meta:
        verbose_name = 'User Experience'
        verbose_name_plural = 'User Experiences'
        
class OTPModel(models.Model):
    otp              = models.CharField(max_length = 6)
    email_linked     = models.EmailField()
    phone_linked     = models.CharField(max_length = 10)
    time_created     = models.IntegerField()

    def __str__(self):
        return f"{self.phone_linked} : {self.otp}"
    class Meta:
        verbose_name = 'OTP Model'
        verbose_name_plural = 'OTP Models'