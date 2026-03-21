from django.urls import path
from . import views
app_name = 'management'

urlpatterns = [
    path('app-settings/', views.AppSettingsView.as_view(), name='app-settings'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]