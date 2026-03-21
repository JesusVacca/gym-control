from django import forms
from django.utils import timezone

from apps.sales.models import CashOpening

class CashOpeningForm(forms.ModelForm):
    class Meta:
        model = CashOpening
        fields = ['amount', 'is_open']
        widgets = {
            'amount': forms.TextInput(attrs={'placeholder': 'Ej: 500000'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        today = timezone.localdate()
        qs = CashOpening.objects.filter(
                created_at__date=today,
                is_open=True
        )
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            self.add_error('amount', 'Ya existe una caja abierta hoy.')
        return cleaned_data