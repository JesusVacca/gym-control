from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from apps.accounts.forms import MemberForm
from apps.accounts.models import Member
from .base_view import BaseDeleteViewMixin, BaseToggleViewMixin
from utils import role_required


@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR,]), name='dispatch')
class TeamListView(ListView):
    template_name = 'members/list.html'
    context_object_name = 'list'
    model = Member

    def get_queryset(self):
        return Member\
            .objects\
            .filter(role__in=[Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY])\
            .exclude(pk=self.request.user.pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse('accounts:team-create')
        context['update_url'] = 'accounts:team-update'
        context['delete_url'] = 'accounts:team-delete'
        context['toggle_url'] = 'accounts:team-toggle'
        context['title'] = 'Personal del gimnasio'
        context['subtitle'] = 'En esta sección puedes encontrar la información deñ personal del gimnasio'
        return context


@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR,]), name='dispatch')
class TeamCreateView(CreateView):
    template_name = 'members/create.html'
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy('accounts:teams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Crear miembro del equipo'
        context['back_url'] = reverse('accounts:teams')
        context['title'] = title
        context["breadcrumbs"] = [
            ("Personal del gimnasio", reverse("accounts:teams")),
            (title, None)
        ]
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['all_role'] = True
        return kwargs

@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR]), name='dispatch')
class TeamUpdateView(UpdateView):
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy('accounts:teams')
    template_name = 'members/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Actualizar miembro del equipo'
        context['back_url'] = reverse('accounts:teams')
        context['title'] = title
        context["breadcrumbs"] = [
            ("Personal del gimnasio", reverse("accounts:teams")),
            (title, None)
        ]
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['all_role'] = True
        return kwargs

@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR]), name='dispatch')
class TeamDeleteViewMixin(BaseDeleteViewMixin):
    model = Member
    redirect_url = 'accounts:teams'


@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR]), name='dispatch')
class TeamToggleView(BaseToggleViewMixin):
    model = Member
    redirect_url = 'accounts:teams'