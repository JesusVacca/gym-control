from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, TemplateView

from apps.accounts.forms import ChangePasswordForm
from apps.accounts.models import Member
from utils import Notify


class MyLoginView(View):
    template_name = 'auth/login.html'
    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )
    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        auth = authenticate(request, username=username, password=password)
        if auth and auth.role in [Member.BaseRoles.SECRETARY, Member.BaseRoles.ADMINISTRATOR]:
            login(request, auth)
            return redirect('management:dashboard')
        Notify.notify(
            request=request,
            message='Usuario y/o contrasela incorrecta',
            level='error',
        )
        return self.get(request)


@method_decorator(
    login_required(login_url='accounts:login'),
    name='dispatch'
)
class ChangePasswordView(UpdateView):
    model = Member
    template_name = 'auth/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('management:dashboard')

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            update_session_auth_hash(self.request, self.object)
            Notify.notify(
                request=self.request,
                message='Contraseña actualizada correctamente',
            )
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(
    login_required(login_url='accounts:login'),
    name='dispatch'
)
class MyProfileView(TemplateView):
    template_name = 'auth/my-profile.html'

@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    return redirect('accounts:login')