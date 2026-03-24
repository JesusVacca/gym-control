from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.memberships.models import Membership

class Command(BaseCommand):
    help = 'Expired memberships'
    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        self.stdout.write('Expired memberships')
        Membership\
            .objects\
            .filter(end_date__lt=today).\
            exclude(status=Membership.Status.EXPIRED).\
            update(status=Membership.Status.EXPIRED)

