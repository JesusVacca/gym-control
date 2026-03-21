from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from apps.memberships.models import Membership

class Notification:
    @staticmethod
    def send_notification(*,subject, message, from_email, recipient_list, fail_silently=False):
        print('Enviando notificaciones')

    @staticmethod
    def send_membership_expiration_notification(*,day_before = 4):
        today = timezone.now().date()
        target_day = today + timedelta(days=day_before)
        memberships = Membership.objects.filter(
            end_date=target_day,
            status=Membership.Status.ACTIVE,
        ).select_related('member','plan')
        for membership in memberships:
            client = membership.member
            if not client.email:continue
            Notification.send_notification(
                subject='Tu membresía está por vencer.',
                message=(
                    f'Hola {client.full_name}, \n\n'
                    f'Tu membresía {membership.plan.name} vence el {membership.end_date}.\n'
                    f'Te recomendamos renovarla.'
                    'Gracias'
                ),
                from_email=client.email,
                recipient_list=[client.email],
            )

    @staticmethod
    def notify_memberships_once_per_day():
        if cache.get('membership_notifications_today'):
            cache.delete('membership_notifications_today')
        if not cache.get('membership_notifications_today'):
            Notification.send_membership_expiration_notification()
            cache.set('membership_notifications_today', True, 60 * 60 * 24)

