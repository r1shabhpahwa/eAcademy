# Generated by Django 4.2.3 on 2023-07-23 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eAcademyApp', '0009_rename_student_userprofile_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='course_images/'),
        ),
    ]
