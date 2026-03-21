from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.dispatch import receiver

from apps.sales.models import CashOpening

@receiver(user_logged_in)
def closed_cash_opening(sender, **kwargs):
    today = timezone.localdate()
    CashOpening\
        .objects\
        .filter(is_open=True)\
        .exclude(created_at__date=today)\
        .update(is_open=False)