from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render
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
    form=McqModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form=McqModelForm()
        obj=Mcq_Skills.objects.get(activated=False)
        with open(obj.mcq_file.path,'r') as f:
            reader=csv.reader(f)

            for i,row in enumerate(reader):
                if i==0:
                    pass
                else:
                    #row = "".join(row)
                    #row=row.split()
                    question=row[0]
                    answer=row[1]
                    s_id=row[2]
                    print("1:",question)
                    print("2:",answer)
                    print("3:",s_id)
                    print(row)
                    Ques_Ans.objects.create(
                        ques=question,
                        ans=answer,
                        skill_id=s_id,
                    )
                    #print(row)
        obj.activated=True
        obj.save()
    return render(request, 'mcqs-templates/mcq_form.html',{'form':form})


def mcq_ques(request):
    global qna_dict,skill_set,ques_bank,ans_bank,qna_skill,ques_skill_id,score_dict

    actual_present_skills=['python','java','css']
    actual_absent_skills=['c','sql']
    len_present=len(actual_present_skills)
    

    if request.method=='POST':
        if request.POST.get('skill_submit'):
            for i in range(len_present):
                id_skill=Skills.objects.filter(skill_name=actual_present_skills[i])
                if id_skill.exists:
                    for j in id_skill:
                        get_id=str(j)
                    skill_set.append([get_id,actual_present_skills[i]])

            print(skill_set)
            len_skill_set=len(skill_set)
            for i in range(len_skill_set):
                skill_ques=Ques_Ans.objects.filter(skill_id=skill_set[i][0]).values('ques')
                skill_ans=Ques_Ans.objects.filter(skill_id=skill_set[i][0]).values('ans')
                #print(skill_ques)
                for k in skill_ques:
                    for key, value in k.items():
                        #print(value)
                        ques_bank.append(value)

                for l in skill_ans:
                    for key, value in l.items():
                        ans_bank.append(value)

            for a in range(len_skill_set):
                for b in range(10):
                    qna_skill.append(skill_set[a][1])   
        
            print(qna_skill)
            qna_dict = dict(zip(ques_bank, ans_bank))  
            print(qna_dict)
            ques_skill_id=dict(zip(ques_bank,qna_skill))
            print(ques_skill_id)
            #qna_skill_dict=dict(zip(qna_skill,qna_dict))
            #print(qna_skill_dict)           

            return render(request, 'mcqs-templates/mcq.html',{'present_skills':actual_present_skills,'absent_skills':actual_absent_skills,'qna_dict':qna_dict})

        if request.POST.get('quiz_submit'):
            #print("inside quiz submit")
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
                #print(value)
                #print(f'Answer:{value[2]}')
                #print('----------------------------------------')
                if(option==value[2]):
                    #if(key==ques_skill_id[])
                    tp=ques_skill_id[key]
                    score_dict[tp]+=1
                    score+=1
                count+=1
            print(your_ans)
            print(score_dict)
            
            #your_ans_dict = dict(zip(your_ans, qna_dict))
            #print(your_ans_dict)
            return render(request, 'mcqs-templates/mcq_analytics.html',{'score':score,'len_dict':len_dict,'qna_dict':qna_dict,'your_ans':your_ans})
        
        return render(request, 'mcqs-templates/mcq.html')


    else:
        return render(request, 'mcqs-templates/mcq.html')

    '''
    if request.method=='POST':
        if request.POST.get('skill_submit'):
            skill_key=request.POST.get('skill_name')
            id_skill=Skills.objects.filter(skill_name=skill_key)
            
            for i in id_skill:
                get_id=i
            id_of_skill=get_id
            

            skill_ques=Ques_Ans.objects.filter(skill_id=get_id).values('ques')
            return render(request, 'mcqs-templates/mcq.html',{'skills':id_skill,'mcqs':skill_ques})

        if request.POST.get('quiz_submit'):
            get_id=id_of_skill
            get_id=2
            print(get_id)
            score=0
            ideal_ans=Ques_Ans.objects.filter(skill_id=get_id).values('ans')
            count=1
            for i in ideal_ans:
                for key, value in i.items():
                    j='choice'+str(count)
                    option=request.POST.get(j)
                    print(value)
                    print(f'Answer:{value[2]}')
                    print('----------------------------------------')
                    if(option==value[2]):
                        score+=1
                    count+=1
                    


            return render(request, 'mcqs-templates/mcq.html',{'score':score})

    else:
        return render(request, 'mcqs-templates/mcq.html')
'''

