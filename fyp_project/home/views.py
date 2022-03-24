from django.core.files.storage import FileSystemStorage
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
import io
from .utils import Calendar
from django.utils.safestring import mark_safe
from django.views import generic
from datetime import datetime
from cmath import sin
from xmlrpc.client import Boolean
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import imp
import logging
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render
from .models import Company, Student, Jd, Skills, Event, Placed_Students
from csvs.models import Csv
from csvs.forms import CsvModelForm
from mcqs.views import *
import csv
# import mcqs.views as mq
from nltk.corpus import stopwords
import re
import gensim
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import nltk
import pickle
nltk.download('punkt')
nltk.download('stopwords')


def home(request):
    return render(request, 'home-templates/home.html')


'''
def placecom_homepage(request):
    return render(request, 'home-templates/placecom_homepage.html')
'''


def schedule(request, roles_id):
    role = Jd.objects.filter(pk=roles_id)[:1].get()
    if request.method == 'POST':
        event = Event()
        event.event_type = request.POST.get('event_type')
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time')
        event.role_id = role
        event.save()
        messages.success(request, f'New Event Scheduled!')
        return render(request, 'home-templates/schedule.html', {'role': role})
    return render(request, 'home-templates/schedule.html', {'role': role})


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
    display_roles = False
    if request.method == 'POST':
        if request.POST.get("single_role") == "single_role":
            display_roles = True
        if request.POST.get("multiple_role") == "multiple_role":
            display_roles = False
            dict_jd_id_skill = {}
            for i in job_roles:
                dict_jd_id_skill[i.id] = i.job_desc

            skills = request.POST.get('skills')
            id_similarity = dict()
            for id, jd in dict_jd_id_skill.items():
                filedocument = sentence_tokenize(jd)

                gen_docs = [[w.lower() for w in word_tokenize(text)]
                            for text in filedocument]
                sw = set(stopwords.words('english'))
                gen_docs = [[w for w in list if w not in sw]
                            for list in gen_docs]

                gen_docs = alphabet_tokenize(gen_docs)
                dictionary = gensim.corpora.Dictionary(gen_docs)
                gen_docs = single_words(gen_docs)
                corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
                len_gen = len(gen_docs)
                tf_idf = gensim.models.TfidfModel(corpus)
                sims = gensim.similarities.Similarity(
                    ".\similarity", tf_idf[corpus], num_features=len(dictionary))

                filedocument2 = sentence_tokenize(skills)

                gen_docs2 = [[w.lower() for w in word_tokenize(text)]
                             for text in filedocument2]

                gen_docs2 = [[w for w in list if w not in sw]
                             for list in gen_docs2]

                gen_docs2 = alphabet_tokenize(gen_docs2)
                gen_docs2 = single_words(gen_docs2)
                corpus2 = [dictionary.doc2bow(gen_doc)
                           for gen_doc in gen_docs2]

                query_doc_tf_idf2 = tf_idf[corpus2]
                sum_of_sims = (
                    np.sum(sims[query_doc_tf_idf2], dtype=np.float32))
                percentage_of_similarity = round(
                    float((sum_of_sims/len_gen) * 100))
                if percentage_of_similarity > 100:
                    percentage_of_similarity = 100
                sims.destroy()
                id_similarity[id] = percentage_of_similarity

            best_similarity_ids = []
            for i in range(3):
                max_id = max(id_similarity, key=id_similarity.get)
                best_similarity_ids.append(max_id)
                id_similarity.pop(max_id)
            first_job = Jd.objects.filter(pk=best_similarity_ids[0])
            second_job = Jd.objects.filter(pk=best_similarity_ids[1])
            third_job = Jd.objects.filter(pk=best_similarity_ids[2])

            return render(request, 'home-templates/student.html', {'job_roles': job_roles, 'display_roles': display_roles})
        if request.POST.get("check_compatibility") == 'Check Compatibility':
            skills = request.POST.get('skills')
            # skills = request.FILES['skills'].read()

            # print("****************************************")
            # print(skills)
            # print("****************************************")
            # text = convert_pdf_to_txt(skills)

            # start = 'familiar with'
            # end = 'key projects'
            # header = 'objective'
            job_role = request.POST.get('jobRole')
            jd = Jd.objects.filter(pk=job_role).first()
            jd = jd.get_job_desc()

            filedocument = sentence_tokenize(jd)

            gen_docs = [[w.lower() for w in word_tokenize(text)]
                        for text in filedocument]
            sw = set(stopwords.words('english'))
            gen_docs = [[w for w in list if w not in sw] for list in gen_docs]

            gen_docs = alphabet_tokenize(gen_docs)
            dictionary = gensim.corpora.Dictionary(gen_docs)
            gen_docs = single_words(gen_docs)
            corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
            len_gen = len(gen_docs)
            tf_idf = gensim.models.TfidfModel(corpus)
            sims = gensim.similarities.Similarity(
                ".\similarity", tf_idf[corpus], num_features=len(dictionary))

            filedocument2 = sentence_tokenize(skills)

            gen_docs2 = [[w.lower() for w in word_tokenize(text)]
                         for text in filedocument2]

            gen_docs2 = [[w for w in list if w not in sw]
                         for list in gen_docs2]

            gen_docs2 = alphabet_tokenize(gen_docs2)
            gen_docs2 = single_words(gen_docs2)
            corpus2 = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs2]

            query_doc_tf_idf2 = tf_idf[corpus2]
            sum_of_sims = (np.sum(sims[query_doc_tf_idf2], dtype=np.float32))
            percentage_of_similarity = round(
                float((sum_of_sims/len_gen) * 100))
            if percentage_of_similarity > 100:
                percentage_of_similarity = 100
            sims.destroy()
            absent_skills = []
            present_skills = []
            gen_docs_list = []
            gen_docs_list2 = []

            len(gen_docs2)

            for i in range(len(gen_docs)):
                for j in gen_docs[i]:
                    gen_docs_list.append(j)

            for i in range(len(gen_docs2)):
                for j in gen_docs2[i]:
                    gen_docs_list2.append(j)

            # print(gen_docs_list,gen_docs_list2)
            for i in gen_docs_list:
                if i not in gen_docs_list2:
                    absent_skills.append(i)
                else:
                    present_skills.append(i)

            actual_present_skills = []
            actual_absent_skills = []
            for i in present_skills:
                if Skills.objects.filter(skill_name=i.lower()).exists():
                    actual_present_skills.append(i)
            for i in absent_skills:
                if Skills.objects.filter(skill_name=i.lower()).exists():
                    actual_absent_skills.append(i)

            context = percentage_of_similarity
            return redirect(check_compatibility, context=context, present_skills=actual_present_skills, absent_skills=actual_absent_skills)

        if request.POST.get("resume_to_resume") == 'resume_to_resume':
            job_role = request.POST.get('jobRole')
            jd = Jd.objects.filter(pk=job_role).first()
            # print(jd)
            display_roles = True
            placed_students_skills = []
            placed_skills = Placed_Students.objects.filter(
                jd_id=jd).values('student_id')
            for i in placed_skills:
                student_skill = Student.objects.filter(
                    pk=int(i['student_id'])).first()
                placed_students_skills.append(student_skill.skills)
            # print(placed_students_skills)

            # Comparing Resumes
            check_resume = request.POST.get('skills')
            percentage_list = []
            for i in placed_students_skills:

                filedocument = sentence_tokenize(i)

                gen_docs = [[w.lower() for w in word_tokenize(text)]
                            for text in filedocument]
                sw = set(stopwords.words('english'))
                gen_docs = [[w for w in list if w not in sw]
                            for list in gen_docs]

                gen_docs = alphabet_tokenize(gen_docs)
                dictionary = gensim.corpora.Dictionary(gen_docs)
                gen_docs = single_words(gen_docs)
                corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
                len_gen = len(gen_docs)
                tf_idf = gensim.models.TfidfModel(corpus)
                sims = gensim.similarities.Similarity(
                    ".\similarity", tf_idf[corpus], num_features=len(dictionary))

                filedocument2 = sentence_tokenize(check_resume)

                gen_docs2 = [[w.lower() for w in word_tokenize(text)]
                             for text in filedocument2]

                gen_docs2 = [[w for w in list if w not in sw]
                             for list in gen_docs2]

                gen_docs2 = alphabet_tokenize(gen_docs2)
                gen_docs2 = single_words(gen_docs2)
                corpus2 = [dictionary.doc2bow(gen_doc)
                           for gen_doc in gen_docs2]

                query_doc_tf_idf2 = tf_idf[corpus2]
                sum_of_sims = (
                    np.sum(sims[query_doc_tf_idf2], dtype=np.float32))
                percentage_of_similarity = round(
                    float((sum_of_sims/len_gen) * 100))
                if percentage_of_similarity > 100:
                    percentage_of_similarity = 100
                sims.destroy()
                percentage_list.append(percentage_of_similarity)

            avg_similarity = round(
                float(sum(percentage_list)/len(percentage_list)))
            # print(avg_similarity)
            return render(request, 'home-templates/student.html', {'job_roles': job_roles, 'avg_similarity': avg_similarity, 'selected_job_role': jd,
                                                                   'display_roles': display_roles})

        # return redirect(check_compatibility, context=context, present_skills=actual_present_skills, absent_skills=actual_absent_skills)
        # return redirect(mcqs.views/mcq_ques)

    return render(request, 'home-templates/student.html', {'job_roles': job_roles, 'display_roles': display_roles})


def check_compatibility(request, context, present_skills, absent_skills):
    if request.method == 'POST':
        # print(present_skills)
        return redirect(mcq_ques, present_skills=present_skills, absent_skills=absent_skills)
    return render(request, 'home-templates/check_compatibility.html', {'context': context})
    # return HttpResponse('<h1> Hello </h1>')


def view_roles(request):
    roles_list = Jd.objects.all()
    if request.POST.get('schedule_event'):
        roles_id = request.POST.get('schedule_event')
        # messages.success(request,f'{role_id}')
        return redirect('schedule', roles_id=roles_id)
        # return render(request, 'home-templates/view_roles.html',{'roles_list':roles_list})
    return render(request, 'home-templates/view_roles.html', {'roles_list': roles_list})


def view_student(request):
    student_list = Student.objects.all()
    if request.POST.get('get_student_id'):
        student_id = request.POST.get('get_student_id')
        return redirect('update_student', student_id=student_id)
        # return render(request, 'home-templates/view_student.html', {'student_list': student_list})
    return render(request, 'home-templates/view_student.html', {'student_list': student_list})


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
            # messages.success(request, f'{check_set_company}')
            return render(request, 'home-templates/view_compatibility.html',
                          {'companies_list': companies_list,
                           'roles_list': roles,
                           'check_set_company': check_set_company,
                           'check_display_company': check_display_company})
        if request.POST.get('get_role') == "submit_role":
            role_id = request.POST.get('selected_role')
            student_list = Student.objects.filter(placement='Unplaced')
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
                           'student_list': student_list,
                           'selected_role_id': role_id})

        if request.POST.get('get_students') == "submit_students":
            selected_students = request.POST.getlist('selected_students[]')
            selected_role_id = request.POST.get('selected_role_id')

            return redirect(stfu, selected_students=selected_students, selected_role_id=selected_role_id)
            # messages.success(request, f'{selected_students}')
            # return render(request, 'home-templates/view_compatibility.html',
            #               {
            #                   'check_display_company': check_display_company,
            #                   'check_select_students': check_select_students,
            #                   'check_set_company': check_set_company,
            #               })

        return render(request, 'home-templates/view_compatibility.html',
                      {'companies_list': companies_list,
                       'check_set_company': check_set_company,
                       'check_display_company': check_display_company,
                       'check_select_students': check_select_students})
    else:
        return render(request, 'home-templates/view_compatibility.html', {'companies_list': companies_list, 'check_display_company': check_display_company})


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
        student.placement = 'Unplaced'
        student.skills = request.POST.get('skills')
        student.save()
        messages.success(request, f'Student Added - {student.student_name}!')
        # CHANGE THE RENDER ADDRESS
        return render(request, 'home-templates/add_student.html')
    else:
        return render(request, 'home-templates/add_student.html')


'''
def schedule(request):
    return render(request, 'home-templates/schedule.html')
'''


def view_schedule(request):
    day = datetime.today()
    future_events = Event.objects.filter(start_time__gte=day)
    messages.success(request, f'Student Added - {future_events}!')
    return render(request, 'home-templates/view_schedule.html')


class CalendarView(generic.ListView):
    model = Event
    template_name = 'home-templates/calendar-base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


# hello


@ login_required
def recruiter(request):
    return render(request, 'home-templates/recruiter.html')


def stfu(request, selected_students, selected_role_id):
    selected_role = Jd.objects.filter(id=selected_role_id).first()
    jd = selected_role.get_job_desc()

    num_list = []
    # skill_list = []
    left_quote = False
    right_quote = False
    val = ''
    for i in range(len(selected_students)):

        if selected_students[i] == '\'':
            if not left_quote:
                left_quote = True
                continue
        if selected_students[i] != '\'':
            if left_quote == True and right_quote == False:
                val += selected_students[i]
                if selected_students[i+1] == '\'':
                    right_quote = True
            elif left_quote == True and right_quote == True:

                num_list.append(int(val))
                val = ''
                left_quote = False
                right_quote = False
                continue
            else:
                continue

    student_data_dict = dict()
    id_skill_dict = dict()
    for i in num_list:
        student = Student.objects.filter(pk=int(i)).first()
        id_skill_dict[student.id] = student.skills
        student_data_dict[student.id] = student

    filedocument = sentence_tokenize(jd)

    gen_docs = [[w.lower() for w in word_tokenize(text)]
                for text in filedocument]
    sw = set(stopwords.words('english'))
    gen_docs = [[w for w in list if w not in sw] for list in gen_docs]

    gen_docs = alphabet_tokenize(gen_docs)

    dictionary = gensim.corpora.Dictionary(gen_docs)

    gen_docs = single_words(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    len_gen = len(gen_docs)
    tf_idf = gensim.models.TfidfModel(corpus)

    sims = gensim.similarities.Similarity(
        ".\similarity", tf_idf[corpus], num_features=len(dictionary))

    id_score_dict = dict()
    for id, skills in id_skill_dict.items():

        filedocument2 = sentence_tokenize(skills)

        gen_docs2 = [[w.lower() for w in word_tokenize(text)]
                     for text in filedocument2]

        gen_docs2 = [[w for w in list if w not in sw] for list in gen_docs2]

        gen_docs2 = alphabet_tokenize(gen_docs2)
        gen_docs2 = single_words(gen_docs2)

        corpus2 = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs2]

        query_doc_tf_idf2 = tf_idf[corpus2]
        print(gen_docs2)
        print('**************************************************************')
        print(gen_docs)
        sum_of_sims = (np.sum(sims[query_doc_tf_idf2], dtype=np.float32))
        print(sims[query_doc_tf_idf2])
        percentage_of_similarity = round(
            float((sum_of_sims/len_gen) * 100))
        if percentage_of_similarity > 100:
            percentage_of_similarity = 100
        sims.destroy()
        id_score_dict[id] = percentage_of_similarity

    ordered_id_score_dict = dict(
        sorted(id_score_dict.items(), key=lambda x: x[1], reverse=True))

    student_data = dict()
    for id, score in ordered_id_score_dict.items():
        student_data[student_data_dict[id]] = score

    return render(request, 'home-templates/stfu.html', {'student_data': student_data})


def update_student(request, student_id):
    student = Student.objects.filter(pk=student_id).first()
    roles = Jd.objects.all()
    placed_student = Placed_Students()
    placement_status = student.placement
    placed_details = ""
    placed_company = ""
    if placement_status == "Unplaced":
        check_student_placement_status = True
    else:
        check_student_placement_status = False
        placed_details = Placed_Students.objects.filter(pk=student.id).first()
    role_id = ""
    role_name = ""
    company_name = ""
    for role in roles:
        role_id += str(role.id)
        role_id += ","

        role_name += str(role)
        role_name += ","

        company_name += str(role.company_id)
        company_name += ","

    role_id = role_id[:-1]
    role_name = role_name[:-1]
    company_name = company_name[:-1]

    if request.method == 'POST':
        student.student_name = request.POST.get("student_name")
        student.email = request.POST.get("email")
        student.cgpa = request.POST.get("cgpa")
        student.skills = request.POST.get("skills")
        if check_student_placement_status == True:
            current_status = request.POST.get("placement_status")
            student.placement = current_status
            if current_status == "Placed":
                get_selected_role_id = request.POST.get("selected_role_id")
                selected_role = Jd.objects.filter(
                    pk=get_selected_role_id).first()
                placed_student.student_id = student
                placed_student.jd_id = selected_role
                placed_student.company_id = selected_role.company_id
                placed_student.save()
        get_role_id = request.POST.get("selected_role_id")
        student.save()
        messages.success(request, f'Student Updated!')
        return render(request, 'home-templates/update_student.html', {'student': student, 'roles': roles})

    return render(request, 'home-templates/update_student.html', {'student': student, 'role_id': role_id,
                                                                  'role_name': role_name, 'company_name': company_name,
                                                                  'check_student_placement_status': check_student_placement_status,
                                                                  'placed_details': placed_details})


def tokenize(text):
    # obtains tokens with a least 1 alphabet
    pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
    return pattern.findall(text.lower())


def sentence_tokenize(text):
    filedocument = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        filedocument.append(sentence)
    return filedocument


def alphabet_tokenize(gen_docs):
    gen_doc = []
    line = ''
    for list in gen_docs:
        for i in list:
            line += i + ' '
        r = tokenize(line)
        gen_doc.append(r)
        line = ''
    return gen_doc


def single_words(list):
    my_list = []
    for i in list:
        if len(i) <= 1:
            my_list.append([i[0]])
        else:
            for j in i:
                my_list.append([j])
    return my_list


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    fp.close()
    device.close()
    text = retstr.getvalue()
    retstr.close()
    return text
