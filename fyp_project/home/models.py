import email
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField


class PlacecomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    place_user_name = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name


class Company(models.Model):
    company_name = models.CharField(blank=False, max_length=50, unique=True)

    def __str__(self):
        return self.company_name

    def get_company_id(self):
        return self.id


class Jd(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_role = models.CharField(blank=False, max_length=50)
    job_desc = models.TextField(blank=False)
    package = models.DecimalField(blank=False, max_digits=3, decimal_places=1)

    def __str__(self):
        return self.job_role

    def get_jd_company_id(self):
        return self.company_id

    def get_job_desc(self):
        return self.job_desc
    
    def get_package(self):
        return self.package


# class Student(models.Model):
#     student_name = models.CharField(blank=False, max_length=50)
#     sap_id = models.IntegerField(blank=False, unique=True)
