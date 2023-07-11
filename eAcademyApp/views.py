from django.contrib.auth import login, authenticate
from .forms import ExtendedUserCreationForm, CourseForm
from .models import Membership, Course
from django.shortcuts import render, redirect


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
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            membership_type = form.cleaned_data['membership_type']
            Membership.objects.create(user=user, membership_type=membership_type)
            return redirect('eAcademyApp:login')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'register.html', {'form': form})



def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course.html', {'courses': courses})

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})





