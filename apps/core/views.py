from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

from apps.accounts.models import Client
from apps.attendances.forms import AttendanceForm
from apps.attendances.services import AttendanceService


from utils import Notify


class IndexView(View):
    template_name = 'core/home.html'
    form_class = AttendanceForm
    def get(self, request):
        return render(
            request,
            self.template_name,{
                'form': self.form_class,
            }
        )

    def post(self, request):
        self.form_class = AttendanceForm(request.POST)
        today = timezone.localdate()
        if self.form_class.is_valid():
            query = self.form_class.cleaned_data['query']
            client = Client.objects.filter(
                Q(phone_number__contains=query)|
                Q(document_number__contains=query)
            ).first()
            self.form_class = AttendanceForm
            if not client or not client.is_active:
               Notify.\
                   notify(
                       request=request,
                       message='Cliente no encontrado',
                       level='info'
                    )
               return self.get(request)
            memberships = client.memberships.filter(
                    status='Activa',
                    end_date__gte=today,
                )
            if not memberships.exists():
                Notify. \
                    notify(
                    request=request,
                    message='No tienes una membresía activa',
                    level='error'
                )
                return self.get(request)

            is_registered, message = AttendanceService.register(
                client=client,
            )

            Notify.notify(
                request=request,
                message=message,
            )

            membership = memberships.order_by('end_date').first()
            if membership and membership.debt > 0:
                message = f"Recuerda que aún debes ${membership.debt:,.0f} de membresía".replace(",", ".")
                Notify.notify(request=request, message=message, level='info')

            return self.get(request)


        return self.get(request)




