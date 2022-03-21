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

    def get_jd_id(self):
        return self.id

    def get_jd_role(self):
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


class Student(models.Model):
    student_name = models.CharField(
        blank=False, max_length=50, null=False, default='-')
    sap_id = models.IntegerField(blank=False, unique=True, default=00000000000)
    program = models.CharField(blank=False, max_length=50, default='B Tech')
    branch = models.CharField(blank=False, max_length=50, default='CS')
    year = models.IntegerField(blank=False, default=4)
    division = models.CharField(blank=False, max_length=1, default='E')
    phone_number = models.IntegerField(
        blank=False, unique=True, null=False, default=0000000000)
    email = models.EmailField(blank=False, default='default@email.com')
    cgpa = models.DecimalField(
        blank=False, max_digits=3, decimal_places=2, default=4)
    #  resume = models.FileField()
    placement = models.CharField(max_length=8, default="Unplaced")
    skills = models.TextField(blank=False)

    def __str__(self):
        return self.student_name
    '''
    def get_sap_id(self):
        return self.sap_id
    '''

    # def get_sap_id(self):
    #     return self.sap_id

    # def get_sap_id(self):
    #     return self.sap_id

    # def get_sap_id(self):
    #     return self.sap_id


class Skills(models.Model):
    skill_name = models.CharField(blank=False, max_length=50, unique=True)

    def __str__(self):
        return str(self.id)

    def get_skill_id(self):
        return self.id
class Event(models.Model):
    event_type=models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    role_id = models.ForeignKey(Jd, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class Placed_Students(models.Model):

    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    jd_id = models.ForeignKey(Jd, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
