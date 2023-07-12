from django.urls import path
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
    path('upgrade/<str:membership_type>/', views.upgrade_view, name='upgrade')
]
