from django.db import models
from django.contrib.auth.models import User


# MODELOS PARA CATEGORÍAS Y SUBCATEGORÍAS
class CategoriaServicio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class SubcategoriaServicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)  # Este es el nuevo campo
    categoria = models.ForeignKey(CategoriaServicio, on_delete=models.CASCADE, related_name='subcategorias')

    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"


class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    subcategoria = models.ForeignKey(SubcategoriaServicio, on_delete=models.CASCADE)  # Relación de clave foránea

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Turno(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.cliente} - {self.servicio} - {self.fecha} {self.hora}"


class Disponibilidad(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='disponibilidades')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('servicio', 'fecha', 'hora_inicio')
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f"{self.servicio.nombre} – {self.fecha} {self.hora_inicio:%H:%M}"


class Consulta(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()  # Ahora obligatorio
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
