from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField

# Create your models here.

class Ques_Ans(models.Model):
    ques=models.TextField(blank=False)
    ans=models.TextField(blank=False)
    skill_id=models.TextField(blank=False)

