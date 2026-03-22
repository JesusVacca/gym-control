from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, View

from apps.accounts.models import Member
from apps.memberships.models import Plan
from utils import role_required, Notify


@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]), name='dispatch')
class PlanListView(ListView):
    model = Plan
    context_object_name = 'planes'
    template_name = 'plan/list.html'


@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]), name='dispatch')
class PlanCreateView(CreateView):
    model = Plan
    fields = '__all__'
    template_name = 'plan/create.html'
    success_url = reverse_lazy('memberships:planes')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear plan'
        context['subtitle'] = 'Para crear un plan, por favor llenar los campos requeridos.'
        return context

    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Plan creado correctamente',
        )
        return super().form_valid(form)

@method_decorator(
    role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),
    name='dispatch'
)
class PlanUpdateView(UpdateView):
    model = Plan
    fields = '__all__'
    template_name = 'plan/create.html'
    success_url = reverse_lazy('memberships:planes')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar plan'
        return context

    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Plan actualizado correctamente',
        )
        return super().form_valid(form)


class PlanDeleteView(View):
    def post(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        try:
            plan.delete()
        except Exception:
            Notify.notify(
                request=request,
                message='No es posible eliminar este plan',
                level='error',
            )
        return redirect('memberships:planes')