from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home-templates/home.html')


def student(request):
    return render(request, 'home-templates/student.html')


@login_required
def recruiter(request):
    return render(request, 'home-templates/recruiter.html')
