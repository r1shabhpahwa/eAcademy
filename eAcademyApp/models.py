from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    level_type = models.CharField(max_length=12, choices=LEVEL_CHOICES, default='beginner')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.FileField(upload_to='course_files/')
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            # Resize the uploaded image to a smaller size for better performance
            img = Image.open(self.image.path)

            max_size = (300, 300)
            if img.height > max_size[0] or img.width > max_size[1]:
                img.thumbnail(max_size)
                img.save(self.image.path)


class WeeklyContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_file = models.FileField(upload_to='weekly_content/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - Week {self.week_number}: {self.title}"


class Membership(models.Model):
    MEMBERSHIP_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='bronze')

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency}"


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)

    def __str__(self):
        return self.user.username

    def isteacher(self):
        return self.user_type == 'professor'

    def isstudent(self):
        return self.user_type == 'student'

class CartItem(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"


class InstructorRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"Instructor Request - {self.user.username}"


class Enrollment(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"


class StudentCourse(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    attendance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"


