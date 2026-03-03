from django import forms
from utils import Validator, BaseModelForm
from apps.accounts.models import Member

class MemberForm(BaseModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'role',
            'email',
            'weight',
            'height',
            'photo',
            'password'
        ]
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'phone_number': 'Número de teléfono',
            'email': 'Correo electrónico',
            'password': 'Contraseña',
            'photo': 'Foto',
            'weight': 'Peso',
            'height': 'Altura',
            'role': 'Tipo de usuario',
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', None)
        if not phone_number:
            raise forms.ValidationError('Por favor ingre un número de teléfono')
        if not Validator.validate_phone_number(phone_number):
            raise forms.ValidationError('El número ingresado no cumple con el formato esperado')
        return phone_number
