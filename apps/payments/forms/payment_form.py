from django import forms
from django.db.models import Sum, F, DecimalField, Q
from django.db.models.functions import Coalesce

from apps.core.widgets import DatalistSelect
from apps.memberships.models import Membership
from apps.payments.models import Payment

class PaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.path_param = kwargs.pop('path_param',None)
        super(PaymentForm, self).__init__(*args, **kwargs)
        memberships_queryset = Membership.objects.annotate(
            total_paid=Coalesce(
                Sum("payments__amount"),
                0,
                output_field=DecimalField()
            )
        )
        if self.instance.pk:
            if self.instance.membership:
                memberships_queryset = memberships_queryset.filter(
                    Q(total_paid__lt=F("price")) |
                    Q(pk=self.instance.membership.pk)
                )
            else:
                memberships_queryset = memberships_queryset\
                    .none()
        else:
            memberships_queryset = memberships_queryset.filter(total_paid__lt=F("price"))
        if self.path_param:
            memberships_queryset = memberships_queryset.filter(pk=self.path_param)
            self.fields['membership'].initial = memberships_queryset.first()

        self.fields['membership'].queryset = memberships_queryset
        self.fields['membership'].widget.queryset = memberships_queryset

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount',0)
        membership = cleaned_data.get('membership')
        if amount <= 0:
            self.add_error('amount', 'El monto no debe ser menor o igual a cero (0)')
        if membership and amount:
            debt = membership.debt
            if self.instance.pk:
                original_amount = self.instance.amount or 0
                debt += original_amount
            if amount > debt:
                self.add_error("amount","El monto no puede ser mayor al precio de la membresía.")
        return cleaned_data




    class Meta:
        model = Payment
        fields = ['membership','amount','payment_method']
        labels = {
            'membership':'Selecionar una membresía (Opcional)',
            'amount':'Valor a pagar',
            'payment_method':'Método de pago',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder':'Ej 7000','class':'money-input'}),
            'membership': DatalistSelect()
        }