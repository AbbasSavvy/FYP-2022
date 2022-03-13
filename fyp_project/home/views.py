from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import imp,logging
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render
from .models import Company, Student, Jd



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

def view_student(request):
    student_list=Student.objects.all()
    return render(request, 'home-templates/view_student.html',{'student_list':student_list})

def view_compatibility(request):
    check_display_company=True
    check_set_company=False
    check_select_students=False
    companies_list=Company.objects.all()
    if request.method == 'POST':
        if request.POST.get('check_company')=="submit_company":
            check_set_company=True
            jd_company_id=request.POST.get('company')
            roles=Jd.objects.filter(company_id=jd_company_id)
            messages.success(request,f'{check_set_company}')
            return render(request, 'home-templates/view_compatibility.html',
                                {'companies_list':companies_list,
                                  'roles_list':roles,
                                  'check_set_company':check_set_company,
                                  'check_display_company':check_display_company})
        if request.POST.get('get_role')=="submit_role":
            role_id=request.POST.get('selected_role')
            selected_role=Jd.objects.filter(id=role_id).first()
            student_list=Student.objects.all()
            check_display_company=False
            check_select_students=True
            check_set_company=False
            #Selected role is fetching correct but not readable-CHECK!
            #messages.success(request,f'{selected_role.get_package}')
            return render(request, 'home-templates/view_compatibility.html',
                                {'companies_list':companies_list,
                                'check_display_company':check_display_company,
                                'check_select_students':check_select_students,
                                'check_set_company':check_set_company,
                                'student_list':student_list})

        if request.POST.get('get_students')=="submit_students":
            selected_students=request.POST.getlist('selected_students[]')
            messages.success(request,f'{selected_students}')
            return render(request, 'home-templates/view_compatibility.html',
                                {
                                'check_display_company':check_display_company,
                                'check_select_students':check_select_students,
                                'check_set_company':check_set_company,
                                })

        return render(request, 'home-templates/view_compatibility.html',
                                {'companies_list':companies_list,
                                  'check_set_company':check_set_company,
                                  'check_display_company':check_display_company,
                                  'check_select_students':check_select_students})
    else:
        return render(request, 'home-templates/view_compatibility.html',{'companies_list':companies_list,'check_display_company':check_display_company})

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

def schedule(request):
    return render(request, 'home-templates/schedule.html')


@login_required
def recruiter(request):
    return render(request, 'home-templates/recruiter.html')
