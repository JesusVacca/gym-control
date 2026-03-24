from django.utils.decorators import method_decorator
from django.views.generic import ListView

from apps.accounts.models import Member
from apps.attendances.models import Attendance
from apps.management.models import AppSettings
from utils import role_required, get_today_range


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
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        return context

    def get_queryset(self):
        queryset =  Attendance.objects.select_related('client').all().order_by('-created_at')
        search = self.request.GET.get('search','')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if not start_date and not end_date:
            start, end = get_today_range()
            queryset = queryset.filter(check_in__range=[start, end])
        if start_date:
            queryset = queryset.filter(check_in__gte=start_date)
        if end_date:
            queryset = queryset.filter(check_in__lte=end_date)
        if search:
            queryset = queryset.filter(client__first_name__icontains=search)
        return queryset

    def get_paginate_by(self, queryset):
        app_settings = AppSettings.load()
        return app_settings.elements_per_section