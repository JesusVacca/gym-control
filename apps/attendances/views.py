from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from apps.accounts.models import Member
from apps.attendances.models import Attendance
from utils import role_required


@method_decorator(
    role_required([Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.SECRETARY]),
    name='dispatch'
)
class AttendanceListView(ListView):
    model = Attendance
    context_object_name = 'attendances'
    template_name = 'attendances/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search','')
        context['start_date'] = self.request.GET.get('start_date',None)
        context['end_date'] = self.request.GET.get('end_date',None)
        return context

    def get_queryset(self):
        queryset =  Attendance.objects.select_related('client').all().order_by('-created_at')
        search = self.request.GET.get('search','')
        start_date = self.request.GET.get('start_date',None)
        end_date = self.request.GET.get('end_date',None)
        if not start_date and not end_date:
            queryset = queryset.filter(check_in__date=timezone.localdate())
        if start_date:
            queryset = queryset.filter(check_in__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(check_in__date__lte=end_date)
        if search:
            queryset = queryset.filter(client__first_name__icontains=search)
        return queryset