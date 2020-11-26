# Generated by Django 3.1.2 on 2020-11-26 05:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userauth', '0001_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=50)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(blank=True, default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='userauth.userprofile')),
            ],
            options={
                'verbose_name': 'Academic ',
                'verbose_name_plural': 'Academics',
                'ordering': ('-start_date',),
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now_add=True)),
                ('remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('file_linked', models.FileField(blank=True, max_length=1048576, null=True, upload_to='user/jobs')),
                ('has_been_accepted', models.BooleanField(blank=True, null=True)),
                ('applied_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userauth.userprofile')),
            ],
            options={
                'verbose_name': 'Job Application',
                'verbose_name_plural': 'Job Applications',
            },
        ),
        migrations.CreateModel(
            name='ProfileView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Profile View',
                'verbose_name_plural': 'Profile Views',
            },
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(blank=True, default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_experience', to='userauth.userprofile')),
            ],
            options={
                'verbose_name': 'Work Experience',
                'verbose_name_plural': 'Work Experiences',
                'ordering': ('end_date', 'start_date', '-id'),
            },
        ),
        migrations.CreateModel(
            name='VolunteerExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=50)),
                ('cause', models.CharField(choices=[('Animal Welfare', 'Animal Welfare'), ('Arts and Culture', 'Arts and Culture'), ('Children', 'Children'), ('Civil Rights and Social Action', 'Civil Rights and Social Action'), ('Economic Empowerment', 'Economic Empowerment'), ('Education', 'Education'), ('Environment', 'Environment'), ('Health', 'Health'), ('Human Rights', 'Human Rights'), ('Politics', 'Politics'), ('Poverty Alleviation', 'Poverty Alleviation'), ('Veteran Support', 'Veteran Support'), ('Social Services', 'Social Services'), ('Science and Technology', 'Science and Technology')], default=None, max_length=50)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(blank=True, default=None, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='volunteer_experience', to='userauth.userprofile')),
            ],
            options={
                'verbose_name': 'Volunteer Experience',
                'verbose_name_plural': 'Volunteer Experiences',
                'ordering': ('-start_date',),
            },
        ),
        migrations.CreateModel(
            name='TestScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('test_date', models.DateField(blank=True, default=None, null=True)),
                ('project_url', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('organization_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_organization', to='organization.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test', to='userauth.userprofile')),
            ],
            options={
                'verbose_name': 'Test Score',
                'verbose_name_plural': 'Test Scores',
                'ordering': ('-test_date',),
            },
        ),
        migrations.CreateModel(
            name='SocialProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('tagline', models.CharField(blank=True, max_length=60, null=True)),
                ('background_photo', models.ImageField(blank=True, max_length=1048576, null=True, upload_to='background/')),
                ('dob', models.DateField(blank=True, default=None, null=True)),
                ('profile_url', models.TextField(blank=True, null=True)),
                ('is_private', models.BooleanField(default=False)),
                ('completely_private', models.BooleanField(default=False)),
                ('semi_private', models.BooleanField(default=False)),
                ('current_academia', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_academic', to='profile.education')),
                ('current_industry', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_work', to='profile.workexperience')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='social_profile', to='userauth.userprofile')),
                ('viewer_list', models.ManyToManyField(through='profile.ProfileView', to='userauth.UserProfile')),
            ],
            options={
                'verbose_name': 'Social Profile',
                'verbose_name_plural': 'Social Profiles',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills_list', models.TextField()),
                ('top_skills', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='userauth.userprofile')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(blank=True, default=None, null=True)),
                ('project_url', models.URLField(blank=True, null=True)),
                ('description', models.TextField()),
                ('organization_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_organization', to='organization.organization')),
                ('user', models.ManyToManyField(blank=True, related_name='project', to='userauth.UserProfile')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ('-start_date',),
            },
        ),
        migrations.AddField(
            model_name='profileview',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='profile.socialprofile'),
        ),
        migrations.AddField(
            model_name='profileview',
            name='viewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed', to='userauth.userprofile'),
        ),
        migrations.CreateModel(
            name='LicenseAndCertification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certification_name', models.CharField(max_length=50)),
                ('organization_name', models.CharField(max_length=50)),
                ('issue_date', models.DateField(default=datetime.date.today)),
                ('expiration_date', models.DateField(blank=True, default=None, null=True)),
                ('credential_id', models.TextField(blank=True, max_length=30, null=True)),
                ('credential_url', models.URLField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='userauth.userprofile')),
            ],
            options={
                'verbose_name': 'License And Certification',
                'verbose_name_plural': 'License And Certifications',
                'ordering': ('-issue_date',),
            },
        ),
        migrations.CreateModel(
            name='JobVacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=30)),
                ('is_remote', models.BooleanField(blank=True, default=False)),
                ('location', models.CharField(max_length=50)),
                ('employment_type', models.CharField(choices=[('Fulltime', 'Full-Time'), ('Parttime', 'Part-Time'), ('Internship', 'Internship'), ('Contract', 'Contract'), ('Volunteer', 'Volunteer'), ('Temporary', 'Temporary')], max_length=50)),
                ('description', models.TextField(blank=True)),
                ('file_linked', models.FileField(blank=True, max_length=1048576, null=True, upload_to='user/jobs')),
                ('skills_required', models.CharField(blank=True, max_length=100, null=True)),
                ('industry', models.CharField(max_length=60)),
                ('pay_range', models.CharField(blank=True, max_length=60, null=True)),
                ('posted_at', models.DateField(auto_now_add=True)),
                ('is_closed', models.BooleanField(default=False)),
                ('show_profile', models.BooleanField(default=True)),
                ('external_site_url', models.URLField(blank=True, null=True)),
                ('applicants', models.ManyToManyField(related_name='jobs_applied_to', through='profile.JobApplication', to='userauth.UserProfile')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs_posted', to='userauth.userprofile')),
                ('saved_by', models.ManyToManyField(blank=True, related_name='saved_jobs', to='userauth.UserProfile')),
                ('viewed_by', models.ManyToManyField(blank=True, to='userauth.UserProfile')),
            ],
            options={
                'verbose_name': 'Job Vacancy',
                'verbose_name_plural': 'Job Vacancies',
            },
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.jobvacancy'),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('passed_date', models.DateField(default=datetime.date.today)),
                ('organization_name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_taken', to='userauth.userprofile')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'ordering': ('-passed_date',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='jobapplication',
            unique_together={('applied_by', 'vacancy')},
        ),
    ]
