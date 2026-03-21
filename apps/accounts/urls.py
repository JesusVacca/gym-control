from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('clients/add/', views.ClientCreateView.as_view(), name='client-add'),
    path('clients/delete/<int:pk>/', views.ClientDeleteView.as_view(), name='client-delete'),
    path('clients/update/<int:pk>/', views.ClientUpdateView.as_view(), name='client-update'),
    path('clients/toggle/<int:pk>/', views.ClientToggleView.as_view(), name='client-toggle'),

    # Team urls
    path('teams/', views.TeamListView.as_view(), name='teams'),
    path('teams/add/', views.TeamCreateView.as_view(), name='team-create'),
    path('teams/update/<int:pk>/', views.TeamUpdateView.as_view(), name='team-update'),
    path('teams/delete/<int:pk>/', views.TeamDeleteViewMixin.as_view(), name='team-delete'),
    path('teams/toggle/<int:pk>/', views.TeamToggleView.as_view(), name='team-toggle'),

    # Body measurement url
    path('body-measurement/', views.BodyMeasurementListView.as_view(), name='body-measurement'),
    path('body-measurement/add/', views.BodyMeasurementCreateView.as_view(), name='body-measurement-add'),
    path('body-measurement/details/<int:pk>/', views.BodyMeasurementDetails.as_view(), name='body-measurement-details'),

    # Auth url
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]