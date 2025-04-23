from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente, Turno, Consulta, Disponibilidad

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
