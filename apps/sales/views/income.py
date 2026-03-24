from django.db.models import Sum, Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from apps.accounts.models import Member
from apps.management.models import AppSettings
from apps.sales.models import Income, CashOpening
from utils import Notify, role_required, get_today_range


@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),name='dispatch')
class IncomeListView(ListView):
    model = Income
    context_object_name = 'incomes'
    template_name = 'income/list.html'

    def get_paginate_by(self, queryset):
        app_settings = AppSettings.load()
        return app_settings.elements_per_section

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date, end_date = get_today_range()
        queryset = Income.objects.filter(created_at__range=[start_date, end_date])
        totals = queryset.aggregate(
            gym=Sum('amount', filter=Q(category=Income.IncomeCategory.GYM)),
            refrigerator=Sum('amount', filter=Q(category=Income.IncomeCategory.REFRIGERATOR)),
            coffee=Sum('amount', filter=Q(category=Income.IncomeCategory.COFFEE)),
            herbalife=Sum('amount', filter=Q(category=Income.IncomeCategory.HERBALIFE)),
            protein=Sum('amount', filter=Q(category=Income.IncomeCategory.PROTEIN)),
            transfer=Sum('amount', filter=Q(payment_method=Income.IncomeMethod.TRANSFER)),
            cash=Sum('amount', filter=Q(payment_method=Income.IncomeMethod.CASH)),
            total=Sum('amount')
        )
        context['gym_income'] = totals['gym'] or 0
        context['refrigerator_income'] = totals['refrigerator'] or 0
        context['coffee_income'] = totals['coffee'] or 0
        context['herbalife_income'] = totals['herbalife'] or 0
        context['protein_income'] = totals['protein'] or 0
        context['transfer'] = totals['transfer'] or 0
        context['cash'] = totals['cash'] or 0
        context['total_today'] = totals['total'] or 0

        return context
    def get_queryset(self):
        start_date, end_date = get_today_range()
        return Income.objects.filter(created_at__range=[start_date, end_date]).order_by('-created_at')


@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),name='dispatch')
class IncomeCreateView(CreateView):
    model = Income
    success_url = reverse_lazy('sales:incomes')
    template_name = 'income/create.html'
    fields = '__all__'
    def form_valid(self, form):
        cash_opening = CashOpening.objects.filter(is_open=True).first()
        if not cash_opening:
            Notify.notify(
                request=self.request,
                message='Aún no hay una caja abierta',
                level='error',
            )
            return super().form_invalid(form)
        form.instance.cash_opening = cash_opening
        Notify.notify(
            request=self.request,
            message='Ingreso registrado correctamente',
        )
        return super().form_valid(form)

@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),name='dispatch')
class IncomeUpdateView(UpdateView):
    model = Income
    success_url = reverse_lazy('sales:incomes')
    fields = '__all__'
    template_name = 'income/create.html'
    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Ingreso actualizado correctamente',
        )
        return super().form_valid(form)