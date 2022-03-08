from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('student/', views.student, name='student'),
    path('recruiter/', views.recruiter, name='recruiter'),
    path('add_company/', views.add_company, name='add_company'),
    path('add_role/', views.add_role, name='add_role'),
    path('view_company/', views.view_company, name='view_company'),
    path('view_roles/', views.view_roles, name='view_roles'),
    #path('placecom_homepage/', views.placecom_homepage, name='placecom_homepage'),
]