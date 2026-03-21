from django.db.models import Sum
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from apps.accounts.models import Member
from apps.sales.models import Income, CashOpening
from utils import Notify, role_required


@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),name='dispatch')
class IncomeListView(ListView):
    model = Income
    context_object_name = 'incomes'
    template_name = 'income/list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context['gym_income'] = Income.objects.filter(category = Income.IncomeCategory.GYM, created_at__date=today).aggregate(total=Sum('amount'))['total'] or 0
        context['refrigerator_income'] = Income.objects.filter(category = Income.IncomeCategory.REFRIGERATOR, created_at__date=today).aggregate(total=Sum('amount'))['total'] or 0
        context['coffee_income'] = Income.objects.filter(category = Income.IncomeCategory.COFFEE, created_at__date=today).aggregate(total=Sum('amount'))['total'] or 0
        context['herbalife_income'] = Income.objects.filter(category = Income.IncomeCategory.HERBALIFE, created_at__date=today).aggregate(total=Sum('amount'))['total'] or 0
        context['protein_income'] = Income.objects.filter(category = Income.IncomeCategory.PROTEIN, created_at__date=today).aggregate(total=Sum('amount'))['total'] or 0
        context['total_today'] = Income.objects.filter(created_at__date=today).aggregate(total=Sum('amount'))['total'] or 0
        context['transfer'] = Income.objects.filter(created_at__date=today, payment_method=Income.IncomeMethod.TRANSFER).aggregate(total=Sum('amount'))['total'] or 0
        context['cash'] = Income.objects.filter(created_at__date=today, payment_method=Income.IncomeMethod.CASH).aggregate(total=Sum('amount'))['total'] or 0
        context['cash_opening'] = CashOpening.objects.filter(created_at__date=today).aggregate(total=Sum('amount'))['total']
        return context
    def get_queryset(self):
        today = timezone.localdate()
        return Income.objects.filter(created_at__date=today).order_by('-created_at')


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