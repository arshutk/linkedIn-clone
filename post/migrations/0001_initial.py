# Generated by Django 3.1.2 on 2020-11-12 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Downvoter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('like', 'like'), ('celebrate', 'celebrate'), ('support', 'support'), ('love', 'love'), ('insightful', 'insightful'), ('curious', 'curious')], default='like', max_length=35)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userauth.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('image_linked', models.ImageField(blank=True, max_length=1048576, null=True, upload_to='article/images/')),
                ('video_linked', models.FileField(blank=True, max_length=5242880, null=True, upload_to='article/videos/')),
                ('doc_linked', models.FileField(blank=True, max_length=2621440, null=True, upload_to='article/docs')),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('bookmarked_by', models.ManyToManyField(blank=True, related_name='bookmarked_posts', to='userauth.UserProfile')),
                ('written_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='userauth.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Upvoter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('like', 'like'), ('celebrate', 'celebrate'), ('support', 'support'), ('love', 'love'), ('insightful', 'insightful'), ('curious', 'curious')], default='like', max_length=35)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userauth.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(default=0)),
                ('downvoter', models.ManyToManyField(blank=True, related_name='down_voter', through='post.Downvoter', to='userauth.UserProfile')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='post.post')),
                ('upvoter', models.ManyToManyField(blank=True, related_name='up_voter', through='post.Upvoter', to='userauth.UserProfile')),
            ],
            options={
                'ordering': ('-vote',),
            },
        ),
        migrations.AddField(
            model_name='upvoter',
            name='vote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='up_vote', to='post.vote'),
        ),
        migrations.AddField(
            model_name='downvoter',
            name='vote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='down_vote', to='post.vote'),
        ),
    ]
