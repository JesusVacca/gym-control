from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

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



@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    return redirect('accounts:login')