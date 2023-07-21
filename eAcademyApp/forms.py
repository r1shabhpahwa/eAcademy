from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Membership, Course


class ExtendedUserCreationForm(UserCreationForm):

    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    membership_type = forms.ChoiceField(choices=Membership.MEMBERSHIP_CHOICES, initial='bronze')
    register_as = forms.ChoiceField(choices=(('student', 'Student'), ('professor', 'Professor')))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'membership_type']


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

class StudentUpdateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students')
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        for student in students:
            self.fields[f'attendance_{student.id}'] = forms.IntegerField(
                label=f'Attendance for {student.first_name} {student.last_name}',
                initial=student.attendance,
                min_value=0,
            )

            self.fields[f'grade_{student.id}'] = forms.DecimalField(
                label=f'Grade for {student.first_name} {student.last_name}',
                initial=student.grade,
                min_value=0,
                max_value=100,
                decimal_places=2,
            )
