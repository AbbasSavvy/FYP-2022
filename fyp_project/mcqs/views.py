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

id_of_skill=0

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
                    #print(row[3])
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
    global id_of_skill
    if request.method=='POST':
        if request.POST.get('skill_submit'):
            skill_key=request.POST.get('skill_name')
            id_skill=Skills.objects.filter(skill_name=skill_key)
            
            for i in id_skill:
                get_id=i
            id_of_skill=get_id
            '''
            q=[] #questions
            a=[] #answer
            q_id=[] #skill ques_id
            r=requests.get('https://www.tutorialspoint.com/'+skill_key+'/'+skill_key+'_online_quiz.htm')
            #parsing html
            soup=BeautifulSoup(r.content,'html.parser')
            #print(soup.prettify())
            print(soup.title)

            
            #finding div to extract info
            entry_div = soup.find('div', class_='mui-col-md-6 tutorial-content')
            entry_div_content = entry_div.findAll('div',class_='QA')
            ques_div=entry_div.find_all('div',class_='Q')
            ans_div=entry_div.find_all('div',class_='A')
            print(ques_div)
            print(ans_div)
            

            #cleaning out tags
            lines = entry_div.findAll('p')

            for line in lines:
                print(line.text)

            for line in ques_div:
                sq=line.text.replace('\n'," ")
                q.append(sq)
                print(line.text)
            for line in ans_div:
                sa=line.text.replace('\n',"")
                sa=line.text.replace('Answer :','')
                a.append(sa)
                print(line.text)    
                q_id.append(get_id)

            print(q)
            print(a)
            print(q_id)
            
            #creating a csv file to store data
            data={
                "Question":q,
                "Answer":a,
                "Skill id": q_id,
                }
            df=pd.DataFrame(data)
            writer = pd.ExcelWriter("{}_mcqs.xlsx".format(skill_key), engine='xlsxwriter')
            df.to_excel(writer, index =False)
            writer.save()
            print("data exported to excel file")
            
            #combining with previous file
            file1=pd.read_excel("mcqs_skills.xlsx")
            file2=pd.read_excel(skill_key+"_mcqs.xlsx")
            list_of_files=[file1,file2]
            new_file=pd.concat(list_of_files)
            new_file.to_excel("mcqs_skills.xlsx",index=False)

            

            #converting xlsx file to csv
            read_file=pd.read_excel("mcqs_skills.xlsx")
            read_file.to_csv("mcqs_skills.csv",index=None,header=False,encoding='utf-8')
            print("data exported to csv file")

            #answer column isnt getting added in this
            '''

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
                    

                # print(i)
                # print(f'Answer is: {i.'ans[3]}')
                # print('****************************')

            # print(ideal_ans)
            # for i in range(1,11):
            #     j='choice'+str(i)
            #     option=request.POST.get(j)
            #     #print(option)
            #     #print(ideal_ans[])
            #     if(option==ideal_ans['ans'][3]):
            #         score+=1
                

            return render(request, 'mcqs-templates/mcq.html',{'score':score})

    else:
        return render(request, 'mcqs-templates/mcq.html')

