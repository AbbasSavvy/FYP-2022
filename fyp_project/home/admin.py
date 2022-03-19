from django.contrib import admin
from .models import Jd, Company, PlacecomUser, Student, Event, Skills
# Register your models here.
admin.site.register(PlacecomUser)
admin.site.register(Company)
admin.site.register(Jd)
admin.site.register(Student)
admin.site.register(Skills)
admin.site.register(Event)

