from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from apps.accounts.models import Client
from utils import role_required, Notify
from .base_view import BaseToggleViewMixin, BaseDeleteViewMixin, BaseSearchView
from ..forms import MemberForm
from ...management.models import AppSettings


@method_decorator(role_required([Client.BaseRoles.ADMINISTRATOR, Client.BaseRoles.SECRETARY]), name='dispatch')
class ClientListView(BaseSearchView):
    model = Client
    context_object_name = 'list'
    template_name = 'members/list.html'

    def get_paginate_by(self, queryset):
        app_settings = AppSettings.load()
        return app_settings.elements_per_section
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['toggle_url'] = 'accounts:client-toggle'
        context['update_url'] = 'accounts:client-update'
        context['delete_url'] = 'accounts:client-delete'
        context['current_url'] = reverse('accounts:clients')
        context['create_url'] = reverse('accounts:client-add')
        context['title'] = 'Listado de clientes'
        return context

@method_decorator(role_required([Client.BaseRoles.ADMINISTRATOR, Client.BaseRoles.SECRETARY]), name='dispatch')
class ClientToggleView(BaseToggleViewMixin):
    model = Client
    redirect_url ='accounts:clients'

@method_decorator(role_required([Client.BaseRoles.ADMINISTRATOR, Client.BaseRoles.SECRETARY]), name='dispatch')
class ClientDeleteView(BaseDeleteViewMixin):
    model = Client
    redirect_url ='accounts:clients'

@method_decorator(role_required([Client.BaseRoles.ADMINISTRATOR, Client.BaseRoles.SECRETARY]), name='dispatch')
class ClientCreateView(CreateView):
    model = Client
    form_class = MemberForm
    template_name = 'members/create.html'
    success_url = reverse_lazy('accounts:clients')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Crear cliente'
        context['title'] = title
        context['back_url'] = reverse('accounts:clients')
        context['breadcrumbs'] = [
            ('Listado de clientes',reverse('accounts:clients')),
            (title,None)

        ]
        return context
    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Cliente creado correctamente',
        )
        return super().form_valid(form)

@method_decorator(role_required([Client.BaseRoles.ADMINISTRATOR, Client.BaseRoles.SECRETARY]), name='dispatch')
class ClientUpdateView(UpdateView):
    model = Client
    form_class = MemberForm
    template_name = 'members/create.html'
    success_url = reverse_lazy('accounts:clients')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('accounts:clients')
        return context
    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Cliente actualizado correctamente',
        )
        return super().form_valid(form)
