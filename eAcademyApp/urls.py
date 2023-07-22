from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

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
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('student-management/', views.student_management, name='student_management'),
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

]
