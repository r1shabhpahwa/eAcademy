from django.urls import path
from . import views

app_name = 'eAcademyApp'
urlpatterns = [
    path('', views.homepage, name='homepage'),

]
