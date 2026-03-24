from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from apps.management.models import AppSettings
from apps.sales.models import CashOpening
from apps.sales.forms import CashOpeningForm
from utils import Notify


class CashOpeningListView(ListView):
    model = CashOpening
    context_object_name = 'cash_openings'
    template_name = 'cash_opening/list.html'

    def get_paginate_by(self, queryset):
        app_settings = AppSettings.load()
        return app_settings.elements_per_section


class CashOpeningCreateView(CreateView):
    model = CashOpening
    template_name = 'cash_opening/create.html'
    success_url = reverse_lazy('sales:cash-opening')
    form_class = CashOpeningForm

    def form_valid(self, form):
        form.instance.team = self.request.user
        Notify.notify(
            request=self.request,
            message='Apertura de caja exitosa',
        )
        return super().form_valid(form)


class CashOpeningUpdateView(UpdateView):
    model = CashOpening
    template_name = 'cash_opening/create.html'
    form_class = CashOpeningForm
    success_url = reverse_lazy('sales:cash-opening')

    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Caja actualizada correctamente',
        )
        return super().form_valid(form)
