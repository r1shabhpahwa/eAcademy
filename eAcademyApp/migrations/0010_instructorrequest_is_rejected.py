# Generated by Django 4.2.3 on 2023-07-23 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eAcademyApp', '0009_rename_student_userprofile_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructorrequest',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]
