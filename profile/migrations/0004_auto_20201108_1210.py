# Generated by Django 3.1.2 on 2020-11-08 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
        ('profile', '0003_remove_skill_my_field2'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Skill',
            new_name='Skills',
        ),
    ]
