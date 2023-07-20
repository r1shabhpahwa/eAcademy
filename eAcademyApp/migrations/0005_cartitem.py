# Generated by Django 4.2.3 on 2023-07-20 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eAcademyApp', '0004_student_email_student_first_name_student_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eAcademyApp.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eAcademyApp.student')),
            ],
        ),
    ]
