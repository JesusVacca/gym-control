from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('members/', views.MemberListView.as_view(), name='members'),
    path('members/create/', views.MemberCreateView.as_view(), name='member-create'),
]