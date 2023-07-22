# Generated by Django 4.2.3 on 2023-07-22 05:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eAcademyApp', '0008_course_level_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Student',
            new_name='UserProfile',
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eAcademyApp.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eAcademyApp.userprofile')),
            ],
        ),
    ]
