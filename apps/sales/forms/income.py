from django import forms
from apps.sales.models import Income

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        exclude = ('cash_opening',)
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Ej: 7000'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ej: Botella de agua'}),
        }