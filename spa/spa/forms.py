from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente, Turno, Consulta, Disponibilidad
from django.contrib.auth.forms import AuthenticationForm
import re

# Formulario para Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['telefono']

# Formulario para Turno
class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['servicio', 'fecha', 'hora']

# Formulario de Registro de Usuario
class RegistroUsuarioForm(UserCreationForm):
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nombre', max_length=100, required=True)
    last_name  = forms.CharField(label='Apellido', max_length=100, required=True)
    telefono   = forms.CharField(label='Teléfono', max_length=20, required=False)

    class Meta:
        model  = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Crear Cliente asociado al usuario
            Cliente.objects.create(
                user     = user,
                telefono = self.cleaned_data.get('telefono', '')
            )
        return user

# Formulario de Consulta
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['nombre', 'mensaje']  # Solo los campos necesarios (sin 'servicio')

    # Si deseas agregar validaciones adicionales o personalizar más los campos, puedes hacerlo aquí.


class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = [
            'servicio',
            'fecha',
            'hora_inicio',
            'hora_fin',
        ]
        widgets = {
            'fecha':       forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin':    forms.TimeInput(attrs={'type': 'time'}),
        }

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario',
            'id': 'id_username',
        })
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'id_password',
        })
    )

class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario',
            'id': 'id_username'
        })
    )
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        return telefono
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre',
            'id': 'id_first_name'
        })
    )
    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido',
            'id': 'id_last_name'
        })
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico',
            'id': 'id_email'
        })
    )
    telefono = forms.CharField(
        label="Teléfono (opcional, solo números)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono (opcional, solo números)',
            'id': 'id_telefono',
            'inputmode': 'numeric',
            'pattern': '[0-9]*'
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'id_password1'
        })
    )
    password2 = forms.CharField(
        label="Repetir Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repetir contraseña',
            'id': 'id_password2'
        })
    )

    class Meta:
        model  = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telefono',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Crear Cliente asociado
            Cliente.objects.create(
                user     = user,
                telefono = self.cleaned_data.get('telefono', '')
            )
        return user

from django import forms

class PagoForm(forms.Form):
    METODO_CHOICES = [
        ('debito', 'Tarjeta de débito'),
        ('credito', 'Tarjeta de crédito'),
    ]

    metodo_pago = forms.ChoiceField(
        label="Método de Pago",
        choices=METODO_CHOICES,
    )
    nombre_tarjeta = forms.CharField(
        label="Nombre en la tarjeta",
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    numero_tarjeta = forms.CharField(
        label="Número de tarjeta",
        max_length=19,
        min_length=12,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'#### #### #### ####'
        })
    )
    vencimiento = forms.CharField(
        label="Vencimiento (MM/AA)",
        max_length=5,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'MM/AA',
            'pattern': r'\d{2}/\d{2}'
        })
    )
    codigo_seguridad = forms.CharField(
        label="Código de seguridad",
        max_length=4,
        min_length=3,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'CVC',
            'type':'password'
        })
    )
