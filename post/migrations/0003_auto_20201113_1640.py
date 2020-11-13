# Generated by Django 3.1.2 on 2020-11-13 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20201113_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celebrate',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='celebrate', to='post.post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='post.post'),
        ),
        migrations.AlterField(
            model_name='love',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='love', to='post.post'),
        ),
        migrations.AlterField(
            model_name='support',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='support', to='post.post'),
        ),
    ]
