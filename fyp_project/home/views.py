from xmlrpc.client import Boolean
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import imp,logging
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render
from .models import Company, Student, Jd
from csvs.models import Csv
from csvs.forms import CsvModelForm
import csv

def home(request):
    return render(request, 'home-templates/home.html')

'''
def placecom_homepage(request):
    return render(request, 'home-templates/placecom_homepage.html')
'''

def upload_file_view(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)

        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i == 0:
                    pass
                else:
                    # print(row)
                    Student.objects.create(
                        student_name = row[0].upper(),
                        sap_id = int(row[1]),
                        program = row[2].upper(),
                        branch = row[3].upper(),
                        year = int(row[4]),
                        division = row[5].upper(),
                        phone_number = int(row[6]),
                        email = row[7],
                        cgpa = row[8],
                        placement = row[9],
                    )

                    
            obj.activated = True
            obj.save()
    return render(request, 'csvs-templates/upload_csvs.html', {'form': form})

def student(request):
    return render(request, 'home-templates/student.html')

def view_roles(request):
    roles_list=Jd.objects.all()
    return render(request, 'home-templates/view_roles.html',{'roles_list':roles_list})

def view_student(request):
    student_list=Student.objects.all()
    return render(request, 'home-templates/view_student.html',{'student_list':student_list})

def view_compatibility(request):
    if request.method == 'POST':
        if request.POST.get('check_company') == 'Add Company':
            print('HELLOOOOOOOOOOOOO!!!!!!!!!!!!!!!!')
            messages.success(request, f'user clicked summary')
    companies_list=Company.objects.all()
    return render(request, 'home-templates/view_compatibility.html',{'companies_list':companies_list})

def add_company(request):
    if request.method == 'GET':
        if request.GET.get('company_name'):
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


def add_student(request):
    if request.method == 'POST':
        student = Student()
        student.student_name = request.POST.get('student_name')
        student.sap_id = request.POST.get('sap_id')
        student.program = request.POST.get('program')
        student.branch = request.POST.get('branch')
        student.year = request.POST.get('year')
        student.division = request.POST.get('division')
        student.phone_number = request.POST.get('phone_number')
        student.email = request.POST.get('email')
        student.cgpa = request.POST.get('cgpa')
        student.placement = request.POST.get('placement')
        student.save()
        messages.success(request, f'Student Added - {student.student_name}!')
        #CHANGE THE RENDER ADDRESS
        return render(request, 'home-templates/add_student.html')
    else:
        return render(request, 'home-templates/add_student.html')


@login_required
def recruiter(request):
    return render(request, 'home-templates/recruiter.html')
