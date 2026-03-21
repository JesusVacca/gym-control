from datetime import timedelta
from django.utils import timezone

def get_today_range():
    now = timezone.localtime()
    start_date = now.replace(hour=0, minute=0, second=0 ,microsecond=0)
    end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start_date, end_date


def get_yesterday_range():
    yesterday = timezone.localtime(timezone.now()) - timedelta(days=1)
    start_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start_yesterday, end_yesterday