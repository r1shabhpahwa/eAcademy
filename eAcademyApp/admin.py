from django.contrib import admin
from .models import Course, Membership, Payment, UserProfile, InstructorRequest

admin.site.register(Course)
admin.site.register(Membership)
admin.site.register(Payment)
admin.site.register(UserProfile)
admin.site.register(InstructorRequest)
