from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Membership


def homepage(request):
    return render(request, 'homepage.html')


def login_view(request):
    if request.method == 'POST':
        # Handle login form submission
        # Use the submitted data to authenticate the user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User is authenticated, log in the user
            login(request, user)
            return redirect('eAcademyApp:homepage')
        else:
            # Authentication failed, show an error message
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # Display the login form
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            membership_type = request.POST.get("membership_type")
            Membership.objects.create(user=user, membership_type=membership_type)
            return redirect('eAcademyApp:login')
    else:
        form = UserCreationForm()
        form.fields['membership_type'].widget.choices = Membership.MEMBERSHIP_CHOICES  # Set choices for membership_type field
    return render(request, 'register.html', {'form': form})




