from django.urls import path
from home.views import upload_file_view

app_name = 'csvs'

urlpatterns = [
    path('upload_csv/', upload_file_view, name='upload-view'),
]
