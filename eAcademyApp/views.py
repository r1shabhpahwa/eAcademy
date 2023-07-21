from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
import stripe
import os
# from .models import InstructorRequest
from .forms import ExtendedUserCreationForm, CourseForm, StudentUpdateForm
from .models import Membership, Course, Student, User, CartItem, InstructorRequest

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
            # Check if the user is approved as an instructor
            try:
                instructor_request = InstructorRequest.objects.get(user=user)
                if not instructor_request.is_approved:
                    # If the instructor request is not approved, prevent login and show message
                    messages.warning(request, 'Not yet approved by the Admin. Please wait for approval!')
                    return redirect('eAcademyApp:login')
            except InstructorRequest.DoesNotExist:
                pass  # The user is not an instructor

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
            messages.warning(request, 'Invalid username or password, please try again.')
            return redirect('eAcademyApp:login')
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
            register_as = form.cleaned_data['register_as']

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            # student = Student.objects.create(user=user, user_type='student')
            student = Student.objects.create(user=user, user_type=register_as)

            if register_as == 'professor':
                InstructorRequest.objects.create(user=user)
                messages.info(request, 'Your instructor request has been sent to the admin for approval.')


            # Check if the selected membership type is an upgrade
            if membership_type != 'bronze':
                messages.info(request, 'This is a paid option. Silver costs $10 per month, and Gold is $20 per month.')
                # Redirect to the payment page
                return redirect(reverse('eAcademyApp:payment'))

            Membership.objects.create(user=user, membership_type=membership_type)

            # Feedback message
            messages.info(request,
                          'You have been successfully registered, please login now!')

            # Redirect to the login page
            return redirect(reverse('eAcademyApp:login'))

        else:
            # Print form errors for debugging
            print(form.errors)
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
    if request.user.student.isteacher():
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('eAcademyApp:course_list')
        else:
            form = CourseForm()
        return render(request, 'create_course.html', {'form': form})
    else:
        # Feedback message
        messages.info(request, 'Only instructors are allowed to access this page.')

        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:course_list'))


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
            # Payment handling
            # TODO

            # Perform the upgrade to Silver logic
            user_membership.membership_type = 'silver'
            user_membership.save()
            messages.success(request, 'You have successfully upgraded to Silver membership!')
        elif membership_type == 'gold' and user_membership.membership_type != 'gold':
            # Payment handling
            # TODO

            # Perform the upgrade to Gold logic
            user_membership.membership_type = 'gold'
            user_membership.save()
            messages.success(request, 'You have successfully upgraded to Gold membership!')
        else:
            messages.warning(request, 'You are already subscribed to the selected membership tier.')
    except Membership.DoesNotExist:
        messages.error(request, 'Membership tiers are applicable only for students. ')

    return redirect(reverse('eAcademyApp:membership'))


def student_list(request):
    students = Student.objects.filter(user__student__user_type='student')

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, students=students)
        if form.is_valid():
            for student in students:
                student.attendance = form.cleaned_data[f'attendance_{student.id}']
                student.grade = form.cleaned_data[f'grade_{student.id}']
                student.save()

            # Add a success message to be shown after successful form submission
            messages.success(request, 'Your changes has been successfully saved!')

            # Redirect to the same page after form submission
            return redirect('eAcademyApp:student_list')

    else:
        form = StudentUpdateForm(students=students)

    return render(request, 'student_list.html', {'students': students, 'form': form})


def my_account(request):
    # Retrieve the currently logged-in student user
    student_user = request.user.student

    return render(request, 'my_account.html', {'student_user': student_user})


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


def add_to_cart(request, course_id):
    if request.user.is_authenticated and not request.user.student.isteacher():
        course = get_object_or_404(Course, pk=course_id)
        student = request.user.student

        # Check if the course is not already in the cart to avoid duplicates
        if not CartItem.objects.filter(student=student, course=course).exists():
            cart_item = CartItem(student=student, course=course)
            cart_item.save()

            # Feedback message
            messages.info(request, 'Course added to cart!')
        else:
            # If the course is already in the cart, you can show a different message if you want.
            messages.info(request, 'Course is already in the cart.')

    else:
        messages.warning(request, 'Only students are eligible to buy courses')

    # Redirect to the homepage
    return redirect('eAcademyApp:course_list')


def remove_from_cart(request, course_id):

    # Remove from cart logic
    # TODO

    # Feedback message
    messages.info(request, 'Course removed from cart!')

    # Redirect to the homepage
    return redirect('eAcademyApp:course_list')

@login_required
def cart(request):
    student = request.user.student
    if request.user.is_authenticated and not request.user.student.isteacher():
        cart_items = CartItem.objects.filter(student=student)
    else:
        cart_items = []
    return render(request, 'cart.html', {'cart_items': cart_items})

# @login_required
# @user_passes_test(lambda user: user.is_superuser)
# def instructor_requests_view(request):
#     instructor_requests = InstructorRequest.objects.all()
#     return render(request, 'instructor_requests.html', {'instructor_requests': instructor_requests})
#
#
# def accept_instructor_request_view(request, user_id):
#     return redirect('eAcademyApp:instructor_requests')
#
# def reject_instructor_request_view(request, user_id):
#     return redirect('eAcademyApp:instructor_requests')

# Updated instructor_requests_view to handle approval and rejection
@login_required
@user_passes_test(lambda user: user.is_superuser)
def instructor_requests_view(request):
    instructor_requests = InstructorRequest.objects.all()
    return render(request, 'instructor_requests.html', {'instructor_requests': instructor_requests})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def accept_instructor_request_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        instructor_request = InstructorRequest.objects.get(user=user)
        instructor_request.is_approved = True
        instructor_request.save()
        messages.success(request, f'Instructor request for {user.username} has been approved.')
    except InstructorRequest.DoesNotExist:
        messages.error(request, 'Instructor request not found.')

    return redirect('eAcademyApp:instructor_requests')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def reject_instructor_request_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        instructor_request = InstructorRequest.objects.get(user=user)
        instructor_request.delete()
        messages.success(request, f'Instructor request for {user.username} has been rejected.')
    except InstructorRequest.DoesNotExist:
        messages.error(request, 'Instructor request not found.')

    return redirect('eAcademyApp:instructor_requests')
