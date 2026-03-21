from django.db.models import OuterRef, Subquery
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, View

from apps.accounts.forms import BodyMeasurementForm
from apps.accounts.models import BodyMeasurement, Client
from utils import role_required

@method_decorator(role_required([Client.BaseRoles.ADMINISTRATOR, Client.BaseRoles.SECRETARY]), name='dispatch')
class BodyMeasurementListView(ListView):
    model = BodyMeasurement
    context_object_name = 'list'
    template_name = 'body_measurement/list.html'
    def get_queryset(self):
        last_measurement = BodyMeasurement.objects.filter(
            client=OuterRef("client")
        ).order_by("-created_at")
        return BodyMeasurement.objects.filter(
            pk=Subquery(last_measurement.values('pk')[:1])
        ).select_related("client")


@method_decorator(role_required([Client.BaseRoles.ADMINISTRATOR, Client.BaseRoles.SECRETARY]), name='dispatch')
class BodyMeasurementCreateView(CreateView):
    model = BodyMeasurement
    form_class = BodyMeasurementForm
    success_url = reverse_lazy('accounts:body-measurement')
    template_name = 'body_measurement/create.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear medidas'
        context['subtitle'] = 'En esta sección podrás crear medidas para los clientes'
        context['back_url'] = reverse('accounts:body-measurement')
        return context

@method_decorator(role_required([Client.BaseRoles.ADMINISTRATOR, Client.BaseRoles.SECRETARY]), name='dispatch')
class BodyMeasurementDetails(View):
    template_name = 'body_measurement/details.html'
    def get(self, request, pk):
        client = get_object_or_404(
            Client.objects.prefetch_related('body_measurement'),
            pk=pk,
        )
        measurements = client.body_measurement.order_by("created_at")
        first = measurements.first()
        last = measurements.last()
        change_rate = None
        if first and last and first.weight !=0:
            change_rate = (( last.weight - first.weight) / first.weight) * 100

        return render(
            request,
            self.template_name,{
                'client': client,
                'measurements': measurements,
                'change_rate': f'{change_rate:,.1f}',
            }
        )