from xmlrpc.client import Boolean
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import imp
import logging
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render
from .models import Company, Student, Jd, Skills
from csvs.models import Csv
from csvs.forms import CsvModelForm
import csv
from nltk.corpus import stopwords
import re
import gensim
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import nltk
import pickle
nltk.download('punkt')


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
                        student_name=row[0].upper(),
                        sap_id=int(row[1]),
                        program=row[2].upper(),
                        branch=row[3].upper(),
                        year=int(row[4]),
                        division=row[5].upper(),
                        phone_number=int(row[6]),
                        email=row[7],
                        cgpa=row[8],
                        placement=row[9],
                    )

            obj.activated = True
            obj.save()
    return render(request, 'csvs-templates/upload_csvs.html', {'form': form})


def student(request):
    job_roles = Jd.objects.all()
    if request.method == 'POST':
        # context = {
        #     'skills' : request.POST.get('skills'),
        #     'job_role' : request.POST.get('jobRole')
        # }
        skills = request.POST.get('skills')
        job_role = request.POST.get('jobRole')
        jd = Jd.objects.filter(pk=job_role).first()
        jd = jd.get_job_desc()

        filedocument = []
        sentences = sent_tokenize(jd)
        for sentence in sentences:
            filedocument.append(sentence)

        gen_docs = [[w.lower() for w in word_tokenize(text)]
                    for text in filedocument]
        sw = set(stopwords.words('english'))
        gen_docs = [[w for w in list if w not in sw] for list in gen_docs]

        gen_doc = []
        line = ''
        for list in gen_docs:
            for i in list:
                line += i + ' '
            r = tokenize(line)
            gen_doc.append(r)
            line = ''

        gen_docs = gen_doc
        dictionary = gensim.corpora.Dictionary(gen_docs)

        corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
        len_gen = len(gen_docs)
        tf_idf = gensim.models.TfidfModel(corpus)
        sims = gensim.similarities.Similarity(
            ".\similarity_index\\similarity", tf_idf[corpus], num_features=len(dictionary))

        filedocument2 = []
        sentences = sent_tokenize(skills)
        for sentence in sentences:
            filedocument2.append(sentence)

        gen_docs2 = [[w.lower() for w in word_tokenize(text)]
                     for text in filedocument2]

        gen_docs2 = [[w for w in list if w not in sw] for list in gen_docs2]

        gen_doc2 = []
        line = ''
        for list in gen_docs2:
            for i in list:
                line += i + ' '
            r = tokenize(line)
            gen_doc2.append(r)
            line = ''

        gen_docs2 = gen_doc2

        # dictionary2 = gensim.corpora.Dictionary(gen_docs2)
        corpus2 = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs2]

        query_doc_tf_idf2 = tf_idf[corpus2]
        sum_of_sims = (np.sum(sims[query_doc_tf_idf2], dtype=np.float32))
        percentage_of_similarity = round(
            float((sum_of_sims/len_gen) * 100))
        if percentage_of_similarity > 100:
            percentage_of_similarity = 100

        # print('------------------------------------------------------')
        # print(percentage_of_similarity)
        # print('------------------------------------------------------')

        context = percentage_of_similarity
        return redirect(check_compatibility, context=context)

    return render(request, 'home-templates/student.html', {'job_roles': job_roles})


def check_compatibility(request, context):
    return render(request, 'home-templates/check_compatibility.html', {'context': context})
    # return HttpResponse('<h1> Hello </h1>')


def view_roles(request):
    roles_list = Jd.objects.all()
    return render(request, 'home-templates/view_roles.html', {'roles_list': roles_list})


def view_student(request):
    student_list = Student.objects.all()
    return render(request, 'home-templates/view_student.html', {'student_list': student_list})


'''
def view_compatibility(request):
    check_display_company = True
    check_set_company = False
    check_select_students = False
    companies_list = Company.objects.all()
    if request.method == 'POST':
        if request.POST.get('check_company') == "submit_company":
            check_set_company = True
            jd_company_id = request.POST.get('company')
            roles = Jd.objects.filter(company_id=jd_company_id)
            messages.success(request, f'{check_set_company}')
            return render(request, 'home-templates/view_compatibility.html',
                          {'companies_list': companies_list,
                           'roles_list': roles,
                           'check_set_company': check_set_company,
                           'check_display_company': check_display_company})
        if request.POST.get('get_role') == "submit_role":
            role_id = request.POST.get('selected_role')
            selected_role = Jd.objects.filter(id=role_id).first()
            student_list = Student.objects.all()
            check_display_company = False
            check_select_students = True
            check_set_company = False
            # Selected role is fetching correct but not readable-CHECK!
            # messages.success(request,f'{selected_role.get_package}')
            return render(request, 'home-templates/view_compatibility.html',
                          {'companies_list': companies_list,
                           'check_display_company': check_display_company,
                           'check_select_students': check_select_students,
                           'check_set_company': check_set_company,
                           'student_list': student_list})

        if request.POST.get('get_students') == "submit_students":
            selected_students = request.POST.getlist('selected_students[]')
            messages.success(request, f'{selected_students}')
            return render(request, 'home-templates/view_compatibility.html',
                          {
                              'check_display_company': check_display_company,
                              'check_select_students': check_select_students,
                              'check_set_company': check_set_company,
                          })

        return render(request, 'home-templates/view_compatibility.html',
                      {'companies_list': companies_list,
                       'check_set_company': check_set_company,
                       'check_display_company': check_display_company,
                       'check_select_students': check_select_students})
    else:
        return render(request, 'home-templates/view_compatibility.html', {'companies_list': companies_list, 'check_display_company': check_display_company})
        if request.POST.get('check_company') == 'Add Company':
            print('HELLOOOOOOOOOOOOO!!!!!!!!!!!!!!!!')
            messages.success(request, f'user clicked summary')
            return render(request, 'home-templates/view_compatibility.html',{'companies_list':companies_list})
    companies_list=Company.objects.all()
    return render(request, 'home-templates/view_compatibility.html',{'companies_list':companies_list})
'''


def add_company(request):
    if request.method == 'POST':
        if request.POST.get('company_name'):
            company = Company()
            company.company_name = request.POST.get('company_name')
            company.save()
            messages.success(request, f'Company added-{company.company_name}!')
            return render(request, 'home-templates/add_company.html')
    else:
        return render(request, 'home-templates/add_company.html')


def view_company(request):
    companies_list = Company.objects.all()
    return render(request, 'home-templates/view_company.html', {'companies_list': companies_list})


def add_role(request):
    companies_list = Company.objects.all()
    if request.method == 'POST':
        if request.POST.get('role_company') and request.POST.get('role') and request.POST.get('package') and request.POST.get('jd'):
            role = Jd()

            # Getting company id as foreign key
            role_company = request.POST.get('role_company')
            company_id = Company.objects.get(pk=role_company)
            role.company_id = company_id
            role.job_role = request.POST.get('role')
            role.job_desc = request.POST.get('jd')

            role.package = request.POST.get('package')
            role.save()
            messages.success(request, f'Role added-{role.job_role}!')
            # CHANGE THE RENDER ADDRESS
            return render(request, 'home-templates/add_role.html', {'companies_list': companies_list})
    else:
        return render(request, 'home-templates/add_role.html', {'companies_list': companies_list})


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
        # CHANGE THE RENDER ADDRESS
        return render(request, 'home-templates/add_student.html')
    else:
        return render(request, 'home-templates/add_student.html')


def schedule(request):
    return render(request, 'home-templates/schedule.html')


@login_required
def recruiter(request):
    return render(request, 'home-templates/recruiter.html')


def tokenize(text):
    # obtains tokens with a least 1 alphabet
    pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
    return pattern.findall(text.lower())
