from django.utils import timezone

from apps.attendances.models import Attendance
from utils import get_today_range


class AttendanceService:
    @staticmethod
    def register(*,client):
        today = timezone.localdate()
        start_date, end_date = get_today_range()
        attendance = Attendance.objects.filter(
            client=client,
            check_in__range=[start_date, end_date]
        )
        if attendance:
            return False, 'Entrada ya registrada hoy'
        Attendance.objects.create(
            client=client,
            check_in=today,
        )
        return True, 'Entrada registrada con exito'