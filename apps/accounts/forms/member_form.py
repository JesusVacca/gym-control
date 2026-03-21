from django import forms

from utils import Validator, BaseModelForm
from apps.accounts.models import Member

class MemberForm(BaseModelForm):

    def __init__(self, *args, **kwargs):
        all_role = kwargs.pop('all_role', None)
        super().__init__(*args, **kwargs)

        if not all_role:
            self.fields['role'].choices = [
                (Member.BaseRoles.CUSTOMER, Member.BaseRoles.CUSTOMER.label),
            ]
        else:
            self.fields['role'].choices = [
                (Member.BaseRoles.ADMINISTRATOR, Member.BaseRoles.ADMINISTRATOR.label),
                (Member.BaseRoles.SECRETARY, Member.BaseRoles.SECRETARY.label),
            ]

    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'role',
            'email',
            'photo',
            'document_type',
            'document_number',
            'birthday'
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

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ingresa el nombre del usuario'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ingresa el apellido del usuario'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Ej: 3XXXXXXXXX'}),
            'email':forms.EmailInput(attrs={'placeholder':'ejemplo@gmail.com'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'Ej: 86.6'}),
            'height': forms.NumberInput(attrs={'placeholder': 'Ej: 178'}),
            'document_number': forms.TextInput(attrs={'placeholder': 'Ingresa el documento del usuario'}),
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }


    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', 'None')
        if not phone_number:
            raise forms.ValidationError('Por favor ingrese un número de teléfono')
        if not Validator.validate_phone_number(phone_number):
            raise forms.ValidationError('El número ingresado no cumple con el formato esperado')
        return phone_number

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance and not instance.pk:
            instance.set_password('1234567890')
        if commit:
            instance.save()
        return instance


