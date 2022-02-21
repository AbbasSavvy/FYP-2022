from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home-templates/home.html')

def student(request):
    return render(request, 'home-templates/student.html')

def recruiter(request):
    return render(request, 'home-templates/recruiter.html')