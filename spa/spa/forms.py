from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Disponibilidad

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ConsultaForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu email'})
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tu mensaje', 'rows': 5})
    )

class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = ['fecha', 'hora_inicio', 'hora_fin']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class PagoForm(forms.Form):
    METODOS_PAGO = [
        ('credito', 'Tarjeta de crédito'),
        ('debito', 'Tarjeta de débito'),
    ]
    
    metodo_pago = forms.ChoiceField(
        choices=METODOS_PAGO,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    numero_tarjeta = forms.CharField(
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'pattern': '[0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}',
            'title': 'Ingrese un número de tarjeta válido (16 dígitos agrupados de 4 en 4)',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "").replace(/(.{4})/g, "$1 ").trim()'
        })
    )
    
    fecha_vencimiento = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/AA',
            'pattern': '(0[1-9]|1[0-2])\/[0-9]{2}',
            'title': 'Ingrese una fecha válida en formato MM/AA',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "").replace(/^(.{2})(.*)$/, "$1/$2").substring(0, 5)'
        })
    )
    
    codigo_seguridad = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CVC',
            'pattern': '[0-9]{3,4}',
            'title': 'Ingrese un código de seguridad válido (3 o 4 dígitos)',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'
        })
    )
    
    nombre_titular = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Como aparece en la tarjeta'
        })
    )
    
    def clean_numero_tarjeta(self):
        numero = self.cleaned_data.get('numero_tarjeta')
        # Eliminar espacios y verificar que sean solo dígitos
        numero = numero.replace(' ', '')
        if not numero.isdigit() or len(numero) != 16:
            raise forms.ValidationError("El número de tarjeta debe tener 16 dígitos.")
        return numero
    
    def clean_fecha_vencimiento(self):
        fecha = self.cleaned_data.get('fecha_vencimiento')
        if not '/' in fecha:
            raise forms.ValidationError("El formato debe ser MM/AA")
        
        try:
            mes, anio = fecha.split('/')
            mes = int(mes)
            anio = int(anio)
            
            if mes < 1 or mes > 12:
                raise forms.ValidationError("El mes debe estar entre 01 y 12")
                
            # Validación básica de año (podría mejorarse para verificar que no sea pasado)
            if anio < 0 or anio > 99:
                raise forms.ValidationError("El año debe estar en formato de dos dígitos (AA)")
        except ValueError:
            raise forms.ValidationError("Formato de fecha inválido")
            
        return fecha
    
    def clean_codigo_seguridad(self):
        codigo = self.cleaned_data.get('codigo_seguridad')
        if not codigo.isdigit() or len(codigo) < 3 or len(codigo) > 4:
            raise forms.ValidationError("El código de seguridad debe tener 3 o 4 dígitos.")
        return codigo