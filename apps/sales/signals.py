from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from apps.sales.models import CashOpening
from utils import get_today_range


@receiver(user_logged_in)
def closed_cash_opening(sender, **kwargs):
    start_date, end_date = get_today_range()
    CashOpening\
        .objects\
        .filter(is_open=True)\
        .exclude(created_at__range=[start_date, end_date])\
        .update(is_open=False)