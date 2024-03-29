from django.urls import path
from mcqs.views import mcq_csv, mcq_ques

app_name = 'mcqs'

urlpatterns = [
    path('mcq_form/', mcq_csv, name='mcq_form'),
    path('<present_skills>/<absent_skills>/mcq/', mcq_ques, name='mcq'),
]
