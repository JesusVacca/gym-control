from django import forms
from django.utils import timezone

from apps.accounts.models import Client
from apps.memberships.models import Membership
from apps.core.widgets import DatalistSelect

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = [
            'plan',
            'member',
            'start_date',
            'status'
        ]
        labels = {
            'plan': 'Selecionar un plan',
            'member': 'Buscar cliente',
            'start_date': 'Inicio membresía',
            'status': 'Estado de membresía',
        }
        widgets = {
            'start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                }
            ),
            'frozen_until': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'member': DatalistSelect(queryset=Client.objects.all()),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.localdate()
        if not self.instance.pk:
            self.fields['start_date'].initial = today

    def clean_member(self):
        member = self.cleaned_data['member']
        today = timezone.localdate()
        qs = Membership.objects.filter(member=member, status=Membership.Status.ACTIVE, end_date__gte=today)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            self.add_error('member','Este cliente ya tiene una membresía activa.')

        return member
