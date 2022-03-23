from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render

#from home.views import check_compatibility
from .mcq_form import McqModelForm
from mcqs.models import Mcq_Skills
from qna.models import Ques_Ans
from home.models import Skills
from django.contrib.auth.models import User
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
# Create your views here.

qna_dict={}
ques_skill_id={}
score_dict={}
skill_set=[]
ques_bank=[]
ans_bank=[]
qna_skill=[]

def mcq_csv(request):
    form = McqModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = McqModelForm()
        obj = Mcq_Skills.objects.get(activated=False)
        with open(obj.mcq_file.path, 'r',encoding="UTF-8") as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i == 0:
                    pass
                else:
                    #row = "".join(row)
                    # row=row.split()
                    question = row[0]
                    answer = row[1]
                    s_id = row[2]
                    print("1:", question)
                    print("2:", answer)
                    print("3:", s_id)
                    print(row)
                    # print(row[3])
                    Ques_Ans.objects.create(
                        ques=question,
                        ans=answer,
                        skill_id=s_id,
                    )
                    # print(row)
        obj.activated = True
        obj.save()
    return render(request, 'mcqs-templates/mcq_form.html', {'form': form})


def mcq_ques(request,present_skills,absent_skills):
    global qna_dict,skill_set,ques_bank,ans_bank,qna_skill,ques_skill_id,score_dict

    present_skills=present_skills[1:]
    present_skills=present_skills[:-1]
    present_skills=present_skills.replace("'",'')
    present_skills=present_skills.split(',')
    len_present = len(present_skills)

    absent_skills=absent_skills[1:]
    absent_skills=absent_skills[:-1]
    absent_skills=absent_skills.replace("'",'')
    absent_skills=absent_skills.split(',')
    len_absent = len(absent_skills)

    if request.method == 'POST':
        if request.POST.get('skill_submit'):
            for i in range(len_present):
                present_skills[i]=present_skills[i].lstrip()
                id_skill = Skills.objects.filter(skill_name=present_skills[i])
                print(id_skill)
                print(present_skills[i])
                if id_skill.exists:
                    for j in id_skill:
                        get_id = str(j)
                    skill_set.append([get_id,present_skills[i]])

            print(skill_set)
            len_skill_set = len(skill_set)
            for i in range(len_skill_set):
                skill_ques = Ques_Ans.objects.filter(
                    skill_id=skill_set[i][0]).values('ques')
                skill_ans = Ques_Ans.objects.filter(
                    skill_id=skill_set[i][0]).values('ans')
                # print(skill_ques)
                for k in skill_ques:
                    for key, value in k.items():
                        # print(value)
                        ques_bank.append(value)

                for l in skill_ans:
                    for key, value in l.items():
                        ans_bank.append(value)

            for a in range(len_skill_set):
                for b in range(10):
                    qna_skill.append(skill_set[a][1])

            #print(qna_skill)
            qna_dict = dict(zip(ques_bank, ans_bank))
            #print(qna_dict)
            ques_skill_id=dict(zip(ques_bank,qna_skill))
            #print(ques_skill_id)

            return render(request, 'mcqs-templates/mcq.html', {'present_skills': present_skills, 'absent_skills': absent_skills, 'qna_dict': qna_dict})

        if request.POST.get('quiz_submit'):
            score=0
            count=1
            your_ans=[]
            len_dict=len(qna_dict)

            for i in range(len(skill_set)):
                var=skill_set[i][1]
                score_dict[var]=0

            for key,value in qna_dict.items():
                j='choice'+str(count)
                option=request.POST.get(j)
                your_ans.append(option)
                if(option==value[2]):
                    tp=ques_skill_id[key]
                    score_dict[tp]+=1
                    score+=1
                count+=1

            return render(request, 'mcqs-templates/mcq_analytics.html', {'score': score, 'len_dict': len_dict, 'qna_dict': qna_dict, 'your_ans': your_ans, 'score_dict':score_dict,'present_skills': present_skills, 'absent_skills': absent_skills})

        return render(request, 'mcqs-templates/mcq.html')

    else:
        return render(request, 'mcqs-templates/mcq.html')
