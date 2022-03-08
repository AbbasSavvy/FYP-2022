from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import imp,logging
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render
from .models import Company
from .models import Jd


def home(request):
    return render(request, 'home-templates/home.html')

'''
def placecom_homepage(request):
    return render(request, 'home-templates/placecom_homepage.html')
'''


def student(request):
    return render(request, 'home-templates/student.html')

def view_roles(request):
    roles_list=Jd.objects.all()
    return render(request, 'home-templates/view_roles.html',{'roles_list':roles_list})

def add_company(request):
    if request.method == 'POST':
        if request.POST.get('company_name'):
            company=Company()
            company.company_name= request.POST.get('company_name')
            company.save()
            messages.success(request, f'Company added-{company.company_name}!')
            return render(request, 'home-templates/add_company.html')  
    else:
        return render(request, 'home-templates/add_company.html')



def view_company(request):
    companies_list=Company.objects.all()
    return render(request, 'home-templates/view_company.html',{'companies_list':companies_list})




def add_role(request):
    companies_list=Company.objects.all()
    if request.method == 'POST':
        if request.POST.get('role_company') and request.POST.get('role') and request.POST.get('package') and request.POST.get('jd'):
            role=Jd()

            #Getting company id as foreign key
            role_company=request.POST.get('role_company')
            company_id = Company.objects.get(pk=role_company)
            role.company_id= company_id
            role.job_role= request.POST.get('role')
            role.job_desc= request.POST.get('jd')
            role.package= request.POST.get('package')
            role.save()
            messages.success(request, f'Role added-{role.job_role}!')
            #CHANGE THE RENDER ADDRESS
            return render(request, 'home-templates/add_role.html',{'companies_list':companies_list})
    else:
        return render(request, 'home-templates/add_role.html',{'companies_list':companies_list})


@login_required
def recruiter(request):
    return render(request, 'home-templates/recruiter.html')
