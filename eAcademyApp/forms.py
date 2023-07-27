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
        fields = ['course', 'week_number', 'title', 'description', 'content_file']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter the courses based on the user's instructor status
        if user and user.userprofile.isteacher():
            self.fields['course'].queryset = Course.objects.filter(instructor=user)


class StudentUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students')
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        for student in students:
            self.fields[f'attendance_{student.id}'] = forms.IntegerField(
                label=f'Attendance for {student.student.user.first_name} {student.student.user.last_name}',
                initial=student.attendance,
                min_value=0,
                max_value=100,
                widget=forms.NumberInput(attrs={'class': 'form-control'}),
            )

            self.fields[f'grade_{student.id}'] = forms.DecimalField(
                label=f'Grade for {student.student.user.first_name} {student.student.user.last_name}',
                initial=student.grade,
                min_value=0,
                max_value=100,
                decimal_places=2,
                widget=forms.NumberInput(attrs={'class': 'form-control'}),
            )