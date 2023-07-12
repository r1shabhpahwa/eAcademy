from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse
import stripe

from .forms import ExtendedUserCreationForm, CourseForm
from .models import Membership, Course, Student, User


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
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('eAcademyApp:homepage')

    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password1']
            membership_type = form.cleaned_data['membership_type']

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            student = Student.objects.create(user=user, user_type='student')

            # Check if the selected membership type is an upgrade
            if membership_type != 'bronze':
                messages.info(request, 'This is a paid option. Silver costs $10 per month, and Gold is $20 per month.')
                # Redirect to the payment page
                return redirect(reverse('eAcademyApp:payment'))

            Membership.objects.create(user=user, membership_type=membership_type)

            return redirect('eAcademyApp:login')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('eAcademyApp:homepage')


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


stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_view(request):
    if request.method == 'POST':
        # Retrieve the payment token from the form submission
        token = request.POST.get('stripeToken')

        # Create a charge with Stripe
        try:
            charge = stripe.Charge.create(
                amount=1000,  # Amount in cents
                currency='usd',
                description='Payment',
                source=token,
            )

            # If the charge is successful, handle the success scenario
            if charge.status == 'succeeded':
                # Perform any necessary actions, such as updating the user's membership status

                # Redirect the user to a success page
                return redirect('eAcademyApp:payment_success')

        except stripe.error.CardError as e:
            # Handle any card errors
            error_msg = e.user_message
            return render(request, 'payment.html', {'error': error_msg})

    return render(request, 'payment.html')
