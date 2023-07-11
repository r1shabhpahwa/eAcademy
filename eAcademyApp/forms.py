from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Membership, Course


class ExtendedUserCreationForm(UserCreationForm):
    membership_type = forms.ChoiceField(choices=Membership.MEMBERSHIP_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'membership_type']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'instructor', 'files')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'instructor': forms.Select(attrs={'class': 'form-control'}),
            'files': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
