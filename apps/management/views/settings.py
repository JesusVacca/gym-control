from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from apps.accounts.models import Member
from apps.management.forms import AppSettingsForm
from apps.management.models import AppSettings
from utils import Notify, role_required


@method_decorator(
    role_required([Member.BaseRoles.ADMINISTRATOR]),
    name='dispatch'
)
class AppSettingsView(UpdateView):
    model = AppSettings
    success_url = reverse_lazy('management:app-settings')
    form_class = AppSettingsForm
    template_name = 'management/create.html'


    def get_object(self, queryset=None):
        return AppSettings.load()

    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message="Datos del sistema actualizado con exito",
        )
        return super().form_valid(form)