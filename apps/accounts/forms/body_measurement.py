from django import forms
from apps.accounts.models import BodyMeasurement, Client
from apps.core.widgets import DatalistSelect

class BodyMeasurementForm(forms.ModelForm):
    class Meta:
        model = BodyMeasurement
        fields = '__all__'
        labels = {
            'client':'Selecionar Cliente',
            'weight':'Peso(kg)',
            'biceps':'Medida de biceps (cm)',
            'chest':'Medida del pecho (cm)',
            'high_abdomen':'Medida abdomen alto (cm)',
            'mid_abdomen':'Medida abdomen medio (cm)',
            'lower_abdomen':'Medida abdomen bajo (cm)',
            'tail':'Medida de cola (cm)',
            'leg':'Medida de piernas (cm)',
            'adductor':'Medida de aductor (cm)',
            'calf':'Medida de pantorrillas (cm)',
        }
        widgets = {
            'client': DatalistSelect(queryset=Client.objects.all()),
        }