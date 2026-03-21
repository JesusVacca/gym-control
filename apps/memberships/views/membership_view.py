from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from apps.accounts.models import Member
from apps.memberships.forms import MembershipForm
from apps.memberships.models import Membership
from utils import Notify, role_required


@method_decorator(
    role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),
    name='dispatch'
)
class MembershipListView(ListView):
    model = Membership
    context_object_name = 'memberships'
    template_name = 'memberships/list.html'


@method_decorator(
    role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),
    name='dispatch'
)
class MembershipCreateView(CreateView):
    model = Membership
    template_name = 'memberships/create.html'
    form_class = MembershipForm
    success_url = reverse_lazy('memberships:memberships')

    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Membresía creada correctamente',
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear membresía'
        context['subtitle'] = 'Para crear una membresía, por favor ingresar los datos requeridos.'
        return context

@method_decorator(
    role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),
    name='dispatch'
)
class MembershipUpdateView(UpdateView):
    model = Membership
    template_name = 'memberships/create.html'
    form_class = MembershipForm
    success_url = reverse_lazy('memberships:memberships')
    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Membresía actualizada correctamente',
        )
        return super().form_valid(form)