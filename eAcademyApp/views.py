from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
import stripe
import os

from .forms import ExtendedUserCreationForm, CourseForm
from .models import Membership, Course, Student, User

# Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY


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
            # Check if 'next' parameter exists in the URL
            next_url = request.GET.get('next')
            if next_url:
                # Redirect to the 'next' URL if it exists
                return redirect(next_url)
            else:
                # Redirect to the default homepage if 'next' URL doesn't exist
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


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Handle message data
        # TODO

        # Feedback message
        messages.info(request, 'Thank you for contacting us! Your message has been received and we will get back to you shortly')

        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:homepage'))

    return render(request, 'contact.html')


@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('eAcademyApp:course_list')
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})


@login_required
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
                # TODO

                # Redirect the user to a success page
                return redirect('eAcademyApp:payment_success')

        except stripe.error.CardError as e:
            # Handle any card errors
            error_msg = e.user_message
            return render(request, 'payment.html', {'error': error_msg})

    return render(request, 'payment.html')


@login_required
def membership_view(request):

    try:
        user_membership = Membership.objects.get(user=request.user)
    except Membership.DoesNotExist:
        user_membership = None

    context = {
        'user_membership': user_membership,
    }
    return render(request, 'membership.html', context)


@login_required
def upgrade_view(request, membership_type):
    try:
        user_membership = Membership.objects.get(user=request.user)
        if membership_type == 'silver' and user_membership.membership_type != 'silver':
            # Perform the upgrade to Silver logic
            user_membership.membership_type = 'silver'
            user_membership.save()
            messages.success(request, 'You have successfully upgraded to Silver membership!')
        elif membership_type == 'gold' and user_membership.membership_type != 'gold':
            # Perform the upgrade to Gold logic
            user_membership.membership_type = 'gold'
            user_membership.save()
            messages.success(request, 'You have successfully upgraded to Gold membership!')
        else:
            messages.warning(request, 'You are already subscribed to the selected membership tier.')
    except Membership.DoesNotExist:
        messages.error(request, 'You are not currently subscribed to any membership tier.')

    return redirect(reverse('eAcademyApp:membership'))


def student_list(request):
    students = Student.objects.filter(user__student__user_type='student')
    return render(request, 'student_list.html', {'students': students})


def aboutus(request):
    return render(request, 'aboutus.html')


def serve_course_file(request, file_name):
    file_path = os.path.join('course_files', file_name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(),
                                    content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{file_name}"'
            return response
    else:
        return HttpResponse("File not found", status=404)
