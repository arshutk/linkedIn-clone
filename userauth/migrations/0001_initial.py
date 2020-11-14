# Generated by Django 3.1.2 on 2020-11-13 20:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('active', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OTPModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6)),
                ('email_linked', models.EmailField(max_length=254)),
                ('phone_linked', models.CharField(max_length=10)),
                ('time_created', models.IntegerField()),
            ],
            options={
                'verbose_name': 'OTP Model',
                'verbose_name_plural': 'OTP Models',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('avatar', models.ImageField(blank=True, max_length=1048576, null=True, upload_to='avatar/')),
                ('location', models.CharField(max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=10)),
                ('organization_name', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(blank=True, default=None, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('followers', models.ManyToManyField(blank=True, related_name='_userprofile_followers_+', to='userauth.UserProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
