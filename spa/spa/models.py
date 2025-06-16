from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# MODELOS PARA CATEGORÍAS Y SUBCATEGORÍAS
class CategoriaServicio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class SubcategoriaServicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
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
    subcategoria = models.ForeignKey(SubcategoriaServicio, on_delete=models.CASCADE)
    precio = models.PositiveIntegerField(default=10000)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# Definición de Profesional antes de Turno
class Profesional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profesional')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='profesionales')

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Turno(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.SET_NULL, null=True, blank=True, related_name='turnos')
    fecha = models.DateField()
    hora = models.TimeField()
    comentario = models.TextField(blank=True, null=True, help_text="Comentarios sobre el turno")

    def __str__(self):
        profesional_str = f" con {self.profesional}" if self.profesional else ""
        return f"{self.cliente} - {self.servicio}{profesional_str} - {self.fecha} {self.hora}"


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
    email = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre


# -------------------------------------------
# Modelos de carrito de compras
# -------------------------------------------
class Cart(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    null=True, blank=True,
                                    on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created     = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha    = models.DateField()
    hora     = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('cart','servicio','fecha','hora')