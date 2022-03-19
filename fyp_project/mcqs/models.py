from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField
# Create your models here.

class Mcq_Skills(models.Model):
    mcq_file=models.FileField(upload_to='mcq')
    #uploaded=models.DateTimeField(auto_now_add=True)
    activated=models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"

