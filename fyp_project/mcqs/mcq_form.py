from django import forms
from .models import Mcq_Skills

class McqModelForm(forms.ModelForm):
    class Meta:
        model=Mcq_Skills
        fields=('mcq_file',)