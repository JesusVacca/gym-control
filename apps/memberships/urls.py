from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path('planes/', views.PlanListView.as_view(), name='planes'),
    path('planes/add/', views.PlanCreateView.as_view(), name='plan-create'),
    path('planes/delete/<int:pk>/', views.PlanDeleteView.as_view(), name='plan-delete'),
    path('planes/update/<int:pk>/', views.PlanUpdateView.as_view(), name='plan-update'),

    # Memberships url
    path('memberships/', views.MembershipListView.as_view(), name='memberships'),
    path('memberships/add/', views.MembershipCreateView.as_view(), name='membership-create'),
    path('memberships/update/<int:pk>/', views.MembershipUpdateView.as_view(), name='membership-update'),
]