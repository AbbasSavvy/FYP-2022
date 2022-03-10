from django.db import models
from .validators import validate_file_extension
# Create your models here.

class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs', validators=[validate_file_extension])
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f'File ID: {self.id}'
