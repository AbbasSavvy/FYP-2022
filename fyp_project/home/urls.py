from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('student/', views.student, name='student'),
    path('recruiter/', views.recruiter, name='recruiter'),
]