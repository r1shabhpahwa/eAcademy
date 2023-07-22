from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

app_name = 'eAcademyApp'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/payment/', views.payment_view, name='payment'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.create_course, name='create_course'),
    path('membership/', views.membership_view, name='membership'),
    path('my-grades/', views.my_grades, name='my_grades'),
    path('contact/', views.contact, name='contact'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('student/', views.student_list, name='student_list'),
    path('upgrade/<str:membership_type>/', views.upgrade_view, name='upgrade'),
    path('course_files/<path:file_name>/', views.serve_course_file, name='serve_course_file'),
    path('add_to_cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:course_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('enrollment/', views.enrollment, name='enrollment'),
    path('instructor-requests/', views.instructor_requests_view, name='instructor_requests'),
    path('accept-instructor-request/<int:user_id>/', views.accept_instructor_request_view, name='accept_instructor_request'),
    path('reject-instructor-request/<int:user_id>/', views.reject_instructor_request_view, name='reject_instructor_request'),
    # path('forgot-password/', views.forgot_password, name='forgot_password'),

    # URL pattern for the forgot password feature
    path('accounts/forgot-password/', views.forgot_password, name='forgot_password'),

    # URL patterns for the built-in Django password reset views
    path('accounts/reset-password/', auth_views.PasswordResetView.as_view(
        template_name='reset_password.html',
        email_template_name='reset_password_email.html',
        success_url='/accounts/reset-password/done/'
    ), name='password_reset'),

    path('accounts/reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='reset_password_done.html'
    ), name='password_reset_done'),

    # URL pattern for password reset confirmation view
    path('accounts/reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='reset_password_confirm.html',
        success_url='/accounts/reset-password/complete/'
    ), name='password_reset_confirm'),

    path('accounts/reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='reset_password_complete.html'
    ), name='password_reset_complete'),


    path('confirm-code/', views.confirm_code, name='confirm_code'),
    path('reset-password/', views.reset_password, name='reset_password'),

# path('send-test-email/', views.send_test_email, name='send_test_email'),
]
