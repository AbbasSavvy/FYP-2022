from xml.etree.ElementInclude import include
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import mcqs


urlpatterns = [
    path('', views.home, name='homepage'),
    path('student/', views.student, name='student'),
    path('recruiter/', views.recruiter, name='recruiter'),
    path('add_company/', views.add_company, name='add_company'),
    path('add_role/', views.add_role, name='add_role'),
    path('view_company/', views.view_company, name='view_company'),
    path('view_roles/', views.view_roles, name='view_roles'),
    path('add_student/', views.add_student, name='add_student'),
    path('view_student/', views.view_student, name='view_student'),
    path('view_compatibility/', views.view_compatibility,
         name='view_compatibility'),

    path('<selected_students>/<selected_role_id>/stfu/', views.stfu, name='stfu'),
    path('', include('csvs.urls', namespace='csvs')),
    #path('schedule/', views.schedule, name='schedule'),
    path('<roles_id>schedule/', views.schedule, name='schedule'),

    path('<context>/<present_skills>/<absent_skills>/check_compatibility/',
         views.check_compatibility, name='check_compatibility'),

    #path('placecom_homepage/', views.placecom_homepage, name='placecom_homepage'),

    path('', include('mcqs.urls', namespace='mcqs')),
    # path('admin/',admin.site.urls),
    #path('view_compatibility/', views.view_compatibility, name='view_compatibility'),


    path('view_schedule/', views.view_schedule, name='view_schedule'),
    path('<student_id>update_student/',
         views.update_student, name='update_student'),
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    path('<present_skills>/<absent_skills>/mcq/',
         mcqs.views.mcq_ques, name="mcq_ques"),
    #path('placecom_homepage/', views.placecom_homepage, name='placecom_homepage'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
