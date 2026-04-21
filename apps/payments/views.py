from django.db import transaction, IntegrityError
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from apps.accounts.models import Member
from apps.management.models import AppSettings
from apps.payments.forms import PaymentForm
from apps.payments.models import Payment
from apps.sales.models import Income, CashOpening
from utils import role_required, Notify


@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),name='dispatch')
class PaymentListView(ListView):
    model = Payment
    template_name = 'payments/list.html'
    context_object_name = 'payments'

    def get_paginate_by(self, queryset):
        app_settings = AppSettings.load()
        return app_settings.elements_per_section

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_payment_type'] = self.request.GET.get('selected_payment_type','')
        context['search'] = self.request.GET.get('search','')
        context['payment_type'] = Payment.PaymentMethod.choices
        return context

    def get_queryset(self):
        queryset = Payment.objects.all().order_by('-payment_date')
        selected_payment_type = self.request.GET.get('selected_payment_type')
        search = self.request.GET.get('search','')
        print(selected_payment_type)
        if search:
            queryset = queryset.filter(
                Q(membership__member__first_name__contains=search) |
                Q(membership__member__last_name__contains=search) |
                Q(membership__member__email__contains=search) |
                Q(membership__member__phone_number__contains=search) |
                Q(payment_type__icontains=search),

            )
        if selected_payment_type:
            queryset = queryset.filter(payment_method=selected_payment_type)
        return queryset



@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),name='dispatch')
class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/create.html'
    success_url = reverse_lazy('payments:payments')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar pago'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['path_param'] = self.request.GET.get('q',None)
        return kwargs

    def form_valid(self, form):
        cash_opening = CashOpening.objects.filter(is_open=True).first()
        if not cash_opening:
            Notify.notify(
                request=self.request,
                message='No es posible registrar el pago, no hay cajas activas',
                level='error'
            )
            return super().form_invalid(form)
        with transaction.atomic():
            self.object = form.save()
            try:
                Income.objects.create(
                    payment=self.object,
                    amount=self.object.amount,
                    payment_method=self.object.payment_method,
                    category=Income.IncomeCategory.GYM,
                    description=self.object.payment_type,
                    cash_opening=cash_opening,
                    source=Income.Source.PAYMENT
                )
            except IntegrityError:
                pass
            Notify.notify(
                request=self.request,
                message='Pago registrado correctamente',
            )
        return redirect(self.get_success_url())

@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),name='dispatch')
class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/create.html'
    success_url = reverse_lazy('payments:payments')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar pago'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['path_param'] = self.request.GET.get('q',None)
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        income = Income.objects.filter(payment=self.object).first()
        if income:
            income.amount = self.object.amount
            income.payment_method = self.object.payment_method
            income.description = self.object.payment_type
            income.source = Income.Source.PAYMENT
            income.save()
        return response

@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),name='dispatch')
class PaymentDeleteView(View):
    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        if payment.payments:
            payment.payments.delete()
        payment.delete()
        Notify.notify(
            request=request,
            message='Pago eliminado correctamente',
        )
        return redirect('payments:payments')