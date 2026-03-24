from django import forms
from apps.accounts.models import Member


class ChangePasswordForm(forms.ModelForm):
    aux_password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Ingresa una nueva contraseña',
            }
        )
    )
    password_confirmed = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repite la contraseña',
            }
        )
    )
    class Meta:
        model = Member
        fields = ['aux_password']


    def clean(self):
        clean_data = self.cleaned_data
        aux_password = clean_data['aux_password']
        password_confirmed = clean_data['password_confirmed']

        if not self.instance.pk:
            self.add_error('aux_password','No fue posible cambiar la contraseña')

        if aux_password != password_confirmed:
            self.add_error('aux_password','Las contraseña no coinciden')
            self.add_error('password_confirmed','Las contraseña no coinciden')

        self.instance.set_password(aux_password)

        return clean_data


