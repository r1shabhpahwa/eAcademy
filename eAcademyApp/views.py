from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
import stripe
from decimal import Decimal
import os
import requests
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

# from .models import InstructorRequest
from .forms import ExtendedUserCreationForm, CourseForm, StudentUpdateForm
from .models import Membership, Course, UserProfile, User, CartItem, InstructorRequest, Enrollment, Payment

# Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY


# ========================================================
# Views for all Users
# ========================================================

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
                if instructor_request.is_rejected:
                    # If the instructor request is rejected, prevent login and show message
                    messages.warning(request, 'Your request was denied. Please contact the admin!')
                    return redirect('eAcademyApp:login')
                elif not instructor_request.is_approved:
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
            register_as = form.cleaned_data['register_as']

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

            # Save User Tpe in UserProfile Model
            UserProfile.objects.create(user=user, user_type=register_as)

            # If user is a student, set default membership type as Bronze
            if register_as == 'student':
                membership_type = 'bronze'
                Membership.objects.create(user=user, membership_type=membership_type)
                # Feedback message
                messages.success(request, 'You have been successfully registered, please login now!')

            # If user is a professor, send approval request
            if register_as == 'professor':
                InstructorRequest.objects.create(user=user)
                # Feedback message
                messages.info(request, 'Your instructor request has been sent to the admin for approval.')

            # Redirect to the login page
            return redirect(reverse('eAcademyApp:login'))

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f"Error in {field}: {error}")


    else:
        form = ExtendedUserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('eAcademyApp:homepage')


def course_list(request):
    courses = Course.objects.all()

    # Check if the user is authenticated and retrieve the student instance if available
    user = request.user

    if user.is_authenticated and not user.is_superuser:
        if user.userprofile.isstudent():
            student = user.userprofile

            for course in courses:
                # Add a dynamic attribute 'is_in_cart' to each course
                course.is_in_cart = CartItem.objects.filter(student=student, course=course).exists() if student else False
                course.is_registered = Enrollment.objects.filter(student=student, course=course).exists() if student else False

    return render(request, 'course.html', {'courses': courses, 'user': user})




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


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Prepare the data to send to Formspree
        data = {
            'name': name,
            'email': email,
            'message': message,
            '_subject': 'eAcademy: User Contact Form Submission',
        }

        formspree_endpoint = 'https://formspree.io/f/mwkdpqgn'

        # Make the HTTP POST request to Formspree
        response = requests.post(formspree_endpoint, data=data)

        # Check if the API call was successful (status code 200 means success)
        if response.status_code == 200:
            # Feedback message
            messages.info(request, 'Thank you for contacting us! Your message has been received and we will get back to you shortly')
        else:
            # Handle the case when the API call failed
            messages.error(request, 'Oops! Something went wrong while submitting your message. Please try again later.')

        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:homepage'))

    return render(request, 'contact.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def forgot_password_view(request):
    if request.method == 'POST':
        # Handle the forgot password form submission
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        if user:
            # Send the confirmation code email to the user
            confirmation_code = default_token_generator.make_token(user)
            subject = 'eAcademy Account: Password Reset Confirmation Code'
            message = f"Hi, registered user {email}, " \
                      f"here is your confirmation code to reset password: " \
                      f"{confirmation_code}."
            from_email = 'ecademycorp@gmail.com'  # Replace with your Gmail email address
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=True)
                messages.success(request, f'A confirmation code has been sent to {email}.')
                request.session['reset_email'] = email
            except:
                messages.error(request, 'Failed to send the confirmation code. Please try again later.')
                return render(request, 'ForgotPassword.html')

        else:
            messages.error(request, 'This user does not exist. Enter a valid email id to continue.')
            return render(request, 'ForgotPassword.html')

        # Redirect to the confirm code page
        return redirect(reverse('eAcademyApp:confirm_code'))

    return render(request, 'ForgotPassword.html')


def confirm_code_view(request):
    if request.method == 'POST':
        # Handle the confirmation code form submission
        confirmation_code = request.POST['confirmation_code']
        email = request.session.get('reset_email', None)

        if email:
            user = get_object_or_404(User, email=email)

            # Validate the confirmation code
            if default_token_generator.check_token(user, confirmation_code):
                # If the confirmation code is valid, proceed to the password reset page
                return redirect(reverse('eAcademyApp:reset_password'))
            else:
                # If the confirmation code is invalid, show an error message
                messages.error(request, 'Invalid confirmation code. Please try again.')
        else:
            messages.error(request, 'No email address found in the session. Please try again.')

    return render(request, 'confirm_code.html')


def reset_password_view(request):
    if request.method == 'POST':
        # Handle the password reset form submission
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        email = request.session.get('reset_email', None)

        if email:
            user = get_object_or_404(User, email=email)

            if new_password == confirm_password:
                # If the passwords match, reset the user's password
                user.set_password(new_password)
                user.save()

                # Clear the email from the session
                del request.session['reset_email']

                # Add a success message to be shown on the login page
                messages.success(request, 'Your password has been reset successfully. Please log in with your new password.')
                return redirect(reverse('eAcademyApp:login'))
            else:
                # If the passwords don't match, show an error message
                messages.error(request, 'Passwords do not match. Please try again.')

        else:
            messages.error(request, 'No email address found in the session. Please try again.')

    return render(request, 'ResetPassword.html')

# ========================================================
# Views for Students only
# ========================================================


@login_required
def membership_view(request):
    if request.user.userprofile.isstudent():
        try:
            user_membership = Membership.objects.get(user=request.user)
        except Membership.DoesNotExist:
            user_membership = None

        context = {
            'user_membership': user_membership,
        }
        return render(request, 'membership.html', context)
    else:
        # Feedback message
        messages.info(request, 'Only Students are eligible to access this page.')

        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:homepage'))

def payment_success(request):
    return render(request, 'payment_success.html')
@login_required
def payment_view(request, membership_type, currency):
    if request.user.userprofile.isstudent():
        try:
            # Validate membership type and currency
            membership_types = [choice[0] for choice in Membership.MEMBERSHIP_CHOICES]
            currencies = [choice[0] for choice in Payment.CURRENCY_CHOICES]
            if membership_type not in membership_types or currency not in currencies:
                raise Exception("Invalid combination of membership type and currency selected.")

            if request.method == 'POST':
                # Retrieve the payment token from the form submission
                token = request.POST.get('stripeToken')

                # Determine the amount based on the membership_type and currency
                if membership_type == 'silver':
                    if currency == 'USD':
                        amount = 1000  # $10.00 USD (Amount in cents)
                    elif currency == 'EUR':
                        amount = 900  # €9.00 EUR (Amount in cents)
                    elif currency == 'GBP':
                        amount = 800  # £8.00 GBP (Amount in cents)
                elif membership_type == 'gold':
                    if currency == 'USD':
                        amount = 1500  # $15.00 USD (Amount in cents)
                    elif currency == 'EUR':
                        amount = 1350  # €13.50 EUR (Amount in cents)
                    elif currency == 'GBP':
                        amount = 1200  # £12.00 GBP (Amount in cents)
                else:
                    raise Exception("Invalid combination of membership type and currency selected.")

                # Create the charge using the appropriate amount and currency
                charge = stripe.Charge.create(
                    amount=amount,
                    currency=currency.lower(),
                    description='Payment',
                    source=token,
                )

                # If the charge is successful, handle the success scenario
                if charge.status == 'succeeded':
                    user = request.user
                    try:
                        membership = Membership.objects.get(user=user)
                        membership.membership_type = membership_type
                        membership.save()
                    except Membership.DoesNotExist:
                        Membership.objects.create(user=user, membership_type=membership_type)

                    # Save the payment information in the database
                    amount_in_decimal = Decimal(amount) / 100
                    payment = Payment.objects.create(user=user, amount=amount_in_decimal, currency=currency)
                    payment.save()

                    return redirect('eAcademyApp:payment_success')
                else:
                    messages.error(request, 'Payment was not successful. Please try again.')

            return render(request, 'payment.html', {'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY})
        except Exception as e:
            # Handle any other unexpected errors
            messages.error(request, str(e))
            return redirect(reverse('eAcademyApp:membership'))

    else:
        # Feedback message
        messages.info(request, 'Only Students are eligible to access this page.')
        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:homepage'))

@login_required
def payment_success_view(request):
    return render(request, 'payment_success.html')

@login_required
def upgrade_view(request, membership_type):
    if request.user.userprofile.isstudent():
        try:
            user_membership = Membership.objects.get(user=request.user)
            if membership_type == 'silver' and user_membership.membership_type != 'silver':
                # Redirect to the currency selection page for Silver membership
                return redirect(reverse('eAcademyApp:currency_selection', args=['silver']))

            elif membership_type == 'gold' and user_membership.membership_type != 'gold':
                # Redirect to the currency selection page for Gold membership
                return redirect(reverse('eAcademyApp:currency_selection', args=['gold']))

            else:
                messages.warning(request, 'You are already subscribed to the selected membership tier.')
        except Membership.DoesNotExist:
            messages.error(request, 'Membership tiers are applicable only for students. ')

        return redirect(reverse('eAcademyApp:membership'))
    else:
        # Feedback message
        messages.info(request, 'Only Students are eligible to access this page.')
        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:homepage'))


@login_required
def currency_selection(request, membership_type):
    if request.user.userprofile.isstudent():
        if request.method == 'POST':
            # Retrieve the selected currency from the form submission
            currency = request.POST.get('currency')
            # Redirect to the payment page with the selected currency
            return redirect('eAcademyApp:payment', membership_type=membership_type, currency=currency)
        return render(request, 'currency_selection.html', {'membership_type': membership_type})
    else:
        # Feedback message
        messages.info(request, 'Only Students are eligible to access this page.')
        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:homepage'))

@login_required
def dashboard(request):
    # Check if the user is a student
    if request.user.userprofile.user_type == 'student':
        # Retrieve the currently logged-in student user
        student_user = request.user.userprofile

        # Get the enrollments of the student (courses enrolled by the student)
        enrollments = Enrollment.objects.filter(student=student_user)

        return render(request, 'dashboard.html', {'student_user': student_user, 'enrollments': enrollments})
    else:
        # Feedback message
        messages.info(request, 'Only Students are eligible to access this page.')

        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:homepage'))




@login_required
def cart_view(request):

    if request.user.userprofile.isstudent():
        student = request.user.userprofile
        cart_items = CartItem.objects.filter(student=student)
        return render(request, 'cart.html', {'cart_items': cart_items})
    else:
        # Feedback message
        messages.info(request, 'Only Students are eligible to access this page.')

        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:homepage'))


@login_required
def add_to_cart(request, course_id):
    if request.user.userprofile.isstudent():
        course = get_object_or_404(Course, pk=course_id)
        student = request.user.userprofile

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

    # Redirect to the Course page
    return redirect('eAcademyApp:course_list')


@login_required
def remove_from_cart(request, course_id):
    if request.user.userprofile.isstudent():
        course = get_object_or_404(Course, pk=course_id)
        student = request.user.userprofile

        # Check if the course is in the cart before removing it
        if CartItem.objects.filter(student=student, course=course).exists():
            cart_item = CartItem.objects.filter(student=student, course=course)
            cart_item.delete()

            # Feedback message
            messages.info(request, 'Course removed from cart!')
        else:
            # If the course is not in the cart, show a message indicating that it cannot be removed.
            messages.info(request, 'Course is not in the cart.')

    else:
        messages.warning(request, 'Only students are eligible to buy courses')

    # Get the 'next' parameter from the request (the page where the request was made)
    next_page = request.GET.get('next')

    if next_page:
        # If 'next' parameter exists, redirect to that page
        return redirect(next_page)
    else:
        # If 'next' parameter doesn't exist, redirect to the course list page by default
        return redirect('eAcademyApp:course_list')


@login_required
def checkout(request):
    if request.user.userprofile.isstudent():
        # Retrieve the user profile for the logged-in user
        user_profile = UserProfile.objects.get(user=request.user)

        # Get the courses in the cart for the user
        cart_courses = CartItem.objects.filter(student=user_profile)

        # Calculate the total number of course registrations in the cart
        previous_registrations = Enrollment.objects.filter(student=user_profile).count()

        # Calculate The total number of courses after new registrations
        total_registrations = previous_registrations + cart_courses.count()

        membership = Membership.objects.get(user=request.user)

        # Check if the user is eligible to register for the courses in the cart based on their member type
        max_registrations = 0
        access_levels = []
        if membership.membership_type == 'bronze':
            max_registrations = 2
            access_levels = ['beginner']
        elif membership.membership_type == 'silver':
            max_registrations = 5
            access_levels = ['beginner', 'intermediate']
        elif membership.membership_type == 'gold':
            max_registrations = float('inf')
            access_levels = ['beginner', 'intermediate', 'advanced']

        cart_valid = 0

        if total_registrations > max_registrations:
            cart_valid = 1

        for course in cart_courses:
            if course.course.level_type not in access_levels:
                if cart_valid == 1:
                    cart_valid = 3
                    break
                else:
                    cart_valid = 2
                    break

        context = {
            'user_profile': user_profile,
            'user_membership': membership,
            'cart_courses': cart_courses,
            'previous_registrations': previous_registrations,
            'total_registrations': total_registrations,
            'max_registrations': max_registrations,
            'access_levels': access_levels,
            'cart_valid': cart_valid
        }
        return render(request, 'checkout.html', context)
    else:
        # Feedback message
        messages.info(request, 'Only instructors are allowed to access this page.')

        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:course_list'))

@login_required
def my_courses_view(request):
    user_profile = request.user.userprofile

    if user_profile.isstudent():
        # For students, retrieve the courses they are enrolled in
        enrolled_courses = Enrollment.objects.filter(student=user_profile)
        courses = [enrollment.course for enrollment in enrolled_courses]

        return render(request, 'my_courses.html', {'courses': courses, 'is_student': True})

    elif user_profile.isteacher():
        # For professors, retrieve the courses they have created
        created_courses = Course.objects.filter(instructor=request.user)
        return render(request, 'my_courses.html', {'courses': created_courses, 'is_student': False})

    else:
        # Redirect to the homepage if the user is neither a student nor a professor
        return redirect('eAcademyApp:homepage')



def enrollment(request):

    if request.method == 'POST':

        # Retrieve the user profile for the logged-in user
        user_profile = UserProfile.objects.get(user=request.user)

        # Get the courses in the cart for the user
        cart_courses = CartItem.objects.filter(student=user_profile)

        # Save enrollments in the Enrollment model
        for course_item in cart_courses:
            enrollment = Enrollment.objects.create(student=user_profile, course=course_item.course)
            enrollment.save()

        # Clear the cart after successful enrollment
        cart_courses.delete()

        # Display success message
        messages.success(request, 'Courses successfully enrolled!')

        # Redirect to the homepage
        return redirect('eAcademyApp:homepage')

    else:
        # Feedback message
        messages.info(request, 'You are not allowed to access this page.')

        # Redirect to the homepage
        return redirect(reverse('eAcademyApp:homepage'))

# ========================================================
# Views for all Instructors only
# ========================================================


@login_required
def create_course(request):
    if request.user.userprofile.isteacher():
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                # Feedback message
                messages.info(request, 'New course has been created!')

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
def student_management(request):
    if not request.user.userprofile.isteacher():
        messages.info(request, 'Only instructors are allowed to access this page.')
        return redirect('eAcademyApp:homepage')

    selected_course = None
    students = []

    if request.method == 'GET':
        course_id = request.GET.get('course')
        if course_id:
            selected_course = get_object_or_404(Course, id=course_id)
            students = Enrollment.objects.filter(course=selected_course)

    elif request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('attendance_'):
                student_id = key.split('_')[1]
                student = get_object_or_404(UserProfile, id=student_id)
                student.attendance = int(value)
                student.save()
            elif key.startswith('grade_'):
                student_id = key.split('_')[1]
                student = get_object_or_404(UserProfile, id=student_id)
                student.grade = float(value)
                student.save()

        messages.success(request, 'Your changes have been saved.')

    courses = Course.objects.filter(instructor=request.user)
    context = {
        'courses': courses,
        'selected_course': selected_course,
        'students': students,
    }
    return render(request, 'student_management.html', context)




# ========================================================
# Views for Admin/Staff
# ========================================================


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
        instructor_request.is_rejected = True
        instructor_request.save()
        messages.success(request, f'Instructor request for {user.username} has been rejected.')
    except InstructorRequest.DoesNotExist:
        messages.error(request, 'Instructor request not found.')

    return redirect('eAcademyApp:instructor_requests')