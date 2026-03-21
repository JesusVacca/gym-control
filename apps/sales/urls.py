from django.urls import path
from . import views

app_name = 'sales'
urlpatterns = [
    path('incomes/', views.IncomeListView.as_view(), name='incomes'),
    path('incomes/add/', views.IncomeCreateView.as_view(), name='income-create'),
    path('incomes/update/<int:pk>/', views.IncomeUpdateView.as_view(), name='income-update'),

    path('cash-opening/', views.CashOpeningListView.as_view(), name='cash-opening'),
    path('cash-opening/add/', views.CashOpeningCreateView.as_view(), name='cash-opening-create'),
    path('cash-opening/update/<int:pk>/', views.CashOpeningUpdateView.as_view(), name='cash-opening-update'),

    path('reports/', views.ReportsListView.as_view(), name='reports'),
    path('reports/pdf/', views.ReportsGeneratePDFView.as_view(), name='reports-pdf'),

]