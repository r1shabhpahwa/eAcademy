from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.FileField(upload_to='course_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


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


class Student(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    attendance = models.PositiveIntegerField(default=0)
    grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return self.user.username

    def isteacher(self):
        return self.user_type == 'professor'

    def is_course_in_cart(self, course_id):
        return self.cartitem_set.filter(course_id=course_id).exists()


class CartItem(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"


class InstructorRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)  # New field to track approval status

    def __str__(self):
        return f"Instructor Request - {self.user.username}"

