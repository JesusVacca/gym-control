from django.utils import timezone
from django.contrib.auth import user_logged_in
from django.db.models.signals import post_delete, post_migrate
from django.dispatch import receiver
from apps.accounts.models import Member


@receiver(post_delete, sender=Member)
def delete_member_image(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(save=False)


@receiver(user_logged_in)
def set_login_time(sender, user, request, **kwargs):
    request.session['login_time'] = timezone.now().timestamp()

@receiver(post_migrate)
def default_admin(sender, app_config,  **kwargs):
    if app_config.name != 'apps.accounts':
        return
    email = 'jesus.vacca@gmail.com'
    document_number = '1007899441'
    if not Member.objects.filter(
            email=email,
            document_number=document_number
    ).exists():
        Member.objects.create_superuser(
            first_name='Jesús',
            email=email,
            password='1234567890',
            **{
                'document_number': document_number,
                'phone_number': '3117984621',
                'document_type':Member.DocumentTypes.CC
            }
        )