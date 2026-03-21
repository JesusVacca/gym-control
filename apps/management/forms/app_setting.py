from django import forms
from apps.management.models import AppSettings

class AppSettingsForm(forms.ModelForm):
    class Meta:
        model = AppSettings
        fields = [
            'app_name',
            'app_description',
            'elements_per_section',
            'app_image',
            'app_logo'
        ]
        labels = {
            'app_image':'Imagen principal del sistema',
            'app_logo':'Logo del sistema',
            'elements_per_section':'Elementos listaado por tabla',
            'app_name':'Nombre de la aplicación',
            'app_description':'Descripcion de la aplicación',
        }