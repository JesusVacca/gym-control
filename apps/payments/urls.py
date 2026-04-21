from django.urls import path
from . import views
app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='payments'),
    path('add/', views.PaymentCreateView.as_view(), name='payment-create'),
    path('update/<int:pk>/', views.PaymentUpdateView.as_view(), name='payment-update'),
    path('delete/<int:pk>/', views.PaymentDeleteView.as_view(), name='payment-delete'),

]