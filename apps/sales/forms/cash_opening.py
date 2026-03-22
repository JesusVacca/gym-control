from django import forms
from apps.sales.models import CashOpening
from utils import get_today_range


class CashOpeningForm(forms.ModelForm):
    class Meta:
        model = CashOpening
        fields = ['amount', 'is_open']
        widgets = {
            'amount': forms.TextInput(attrs={'placeholder': 'Ej: 500000'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date, end_date = get_today_range()
        qs = CashOpening.objects.filter(
                created_at__range=[start_date, end_date],
                is_open=True
        )
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            self.add_error('amount', 'Ya existe una caja abierta hoy.')
        return cleaned_data