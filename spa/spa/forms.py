from django import forms
from django.contrib.auth.models import User
from spa.models import Categoria, Posts, Comentario, Cliente, Turno

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono']

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['servicio', 'fecha', 'hora']
