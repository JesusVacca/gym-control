from django.urls import path
from . import views

app_name = 'attendances'
urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='attendances'),
]