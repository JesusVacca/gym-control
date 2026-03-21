from django.db.models import Sum, F
from django.db.models.fields import DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.attendances.models import Attendance
from apps.accounts.models import Client, Member
from apps.memberships.models import Membership
from apps.sales.models import CashOpening, Income

from apps.notifications.notifications import Notification
from utils import role_required, get_today_range
from utils.datetime import get_yesterday_range


@method_decorator(role_required([Member.BaseRoles.ADMINISTRATOR]),name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cash_opening'] = CashOpening.objects.filter(is_open=True).exists()

        # Ingresos del mes
        now = timezone.localtime(timezone.now())
        current_year = now.year
        current_month = now.month
        context['income_month'] = Income.objects.filter(
            created_at__year=current_year,
            created_at__month=current_month
        ).aggregate(total_month=Sum('amount'))['total_month'] or 0

        # Ingresos hoy
        income_today = Income.objects\
            .filter(created_at__range=(get_today_range()))\
            .aggregate(total_today=Sum('amount'))['total_today'] or 0
        # Ingreso ayer
        income_yesterday = Income.objects\
            .filter(created_at__range=(get_yesterday_range()))\
            .aggregate(total_yesterday=Sum('amount'))['total_yesterday'] or 0
        context['income_today'] = income_today

        # Clientes activos
        context['active_clients'] = Client.objects\
            .filter(is_active=True)\
            .count()

        context['attendances_today'] = Attendance.objects.filter(check_in__range=(get_today_range())).count()
        context['new_clients_today'] = Client.objects.filter(created_at__range=(get_today_range())).count()

        # Ultimas membresías
        context['last_memberships'] = Membership.objects.filter(created_at__range=(get_today_range()))[:10]

        # Clientes que deben membresías
        context['clients_with_debts'] = Membership.objects\
            .annotate(total_paid=Coalesce(
                Sum("payments__amount"),
                0,
                output_field=DecimalField()
            ))\
            .filter(total_paid__lt=F('price'), status=Membership.Status.ACTIVE).order_by('created_at')[:10]


        if income_yesterday == 0:
            if income_today == 0:
                context['percentage_variation'] = 0
            else:
                context['percentage_variation'] = None  # o "Nuevo ingreso"
        else:
            context['percentage_variation'] = ((income_today - income_yesterday) / income_yesterday) * 100

        Notification.notify_memberships_once_per_day()
        return context