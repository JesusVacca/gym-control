from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

from apps.accounts.models import Client
from apps.attendances.forms import AttendanceForm
from apps.attendances.models import Attendance


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
        today = timezone.localtime()
        if self.form_class.is_valid():
            query = self.form_class.cleaned_data['query']
            client = Client.objects.filter(
                Q(phone_number__contains=query)
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
            if not client.memberships.filter(
                    status='Activa',
                    end_date__gte=today,
                ).exists():
                Notify. \
                    notify(
                    request=request,
                    message='No tienes una membresía activa',
                    level='error'
                )
                return self.get(request)
            open_attendance = Attendance.objects.filter(
                client=client,
                check_in__date=today
            ).first()
            if open_attendance:
                Notify.notify(request=request, message='Entrada ya registrada hoy')
            else:
                Attendance.objects.create(client=client)
                Notify.notify(request=request, message='Entrada registrada con éxito')

            return self.get(request)


        return self.get(request)




