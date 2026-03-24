from django.core.mail import send_mail
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from apps.memberships.models import Membership

class Notification:
    @staticmethod
    def send_email_notification(*, subject, message, from_email, recipient_list, fail_silently=False):
        send_mail(subject, message, from_email, recipient_list, fail_silently)

    @staticmethod
    def send_membership_expiration_notification(*,day_before = 3):
        today = timezone.localdate()
        target_day = today + timedelta(days=day_before)

        memberships = Membership.objects.filter(
            end_date__range=[today, target_day],
            status=Membership.Status.ACTIVE,
            notified_expiration=False
        ).select_related('member','plan')

        for membership in memberships:
            client = membership.member
            try:
                Notification.send_email_notification(
                    subject='Tu membresía está por vencer.',
                    message=(
                        f'Hola {client.full_name},\n\n'
                        f'Tu membresía {membership.plan.name} vence el {membership.end_date}.\n'
                        f'Te recomendamos renovarla.\n\n'
                        f'Gracias'
                    ),
                    from_email='gimnasiofit8@gmail.com',
                    recipient_list=[client.email],
                )
                membership.notified_expiration = True
                membership.save(update_fields=['notified_expiration'])
            except Exception as e:
                print(f'Error enviando a {client.email}')

    @staticmethod
    def notify_memberships_once_per_day():
        if not cache.get('membership_notifications_today'):
            Notification.send_membership_expiration_notification()
            cache.set('membership_notifications_today', True, 60 * 60 * 24)

