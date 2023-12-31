from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Membership, Course, UserProfile, WeeklyContent


class ExtendedUserCreationForm(UserCreationForm):

    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    register_as = forms.ChoiceField(choices=(('student', 'Student'), ('professor', 'Professor')))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the instructor field queryset to only include professors
        self.fields['instructor'].queryset = User.objects.filter(userprofile__user_type='professor')\
            .select_related('userprofile')

    class Meta:
        model = Course
        fields = ('title', 'level_type', 'description', 'instructor', 'image', 'files', )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'level_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'instructor': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'files': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'level_type': 'Course Level',
            'image': 'Course Image',
            'files': 'Course Outline Document'
        }


class WeeklyContentForm(forms.ModelForm):
    class Meta:
        model = WeeklyContent
        fields = ['course', 'week_number', 'title', 'description', 'content_file','assignment_file']

        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'week_number': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content_file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'assignment_file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),

    }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter the courses based on the user's instructor status
        if user and user.userprofile.isteacher():
            self.fields['course'].queryset = Course.objects.filter(instructor=user)

