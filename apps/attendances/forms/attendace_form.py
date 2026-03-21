from django import forms

class AttendanceForm(forms.Form):
    query = forms.CharField(
        label="Cédula o correo",
        max_length=100,
        widget=forms.NumberInput(
            attrs={'placeholder': 'Ingrese cédula o correo'}
        )
    )