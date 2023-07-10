from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Membership


class ExtendedUserCreationForm(UserCreationForm):
    membership_type = forms.ChoiceField(choices=Membership.MEMBERSHIP_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'membership_type']
