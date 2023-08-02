from django.contrib import admin
from .models import Course, Membership, Payment, UserProfile, InstructorRequest, Enrollment, WeeklyContent,StudentAssignment,StudentCourse

admin.site.register(Course)
admin.site.register(Membership)
admin.site.register(Payment)
admin.site.register(UserProfile)
admin.site.register(InstructorRequest)
admin.site.register(Enrollment)
admin.site.register(WeeklyContent)
admin.site.register(StudentAssignment)
admin.site.register(StudentCourse)
