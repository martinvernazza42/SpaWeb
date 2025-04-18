from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings



# spa/models.p
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    # Ligamos cada Cliente a un User de Django
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        # Usa el nombre completo del User si está, o el username
        return self.user.get_full_name() or self.user.username

class Turno(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.cliente} - {self.servicio} - {self.fecha} {self.hora}"

class Disponibilidad(models.Model):
    servicio    = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='disponibilidades')
    fecha       = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin    = models.TimeField()

    class Meta:
        unique_together = ('servicio', 'fecha', 'hora_inicio')
        ordering        = ['fecha', 'hora_inicio']

    def __str__(self):
        return f"{self.servicio.nombre} – {self.fecha} {self.hora_inicio:%H:%M}"


class Consulta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    mensaje = models.TextField()