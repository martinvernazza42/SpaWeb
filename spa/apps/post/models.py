from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Clase Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

# Clase Posts
class Posts(models.Model):
    titulo = models.CharField(max_length=50)
    subtitulo = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    texto = models.TextField()
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey (Categoria, on_delete= models.SET_NULL, null=True, default='Sin categoría' )  # Ya no es nullable ni tiene default incorrecto
    imagen = models.ImageField(null=True, blank=True, upload_to='media', default='static/post_default.png')
    publicado = models.DateField(default=timezone.now)

    class Meta:
        ordering = ('-publicado',)

    def __str__(self):
        return self.titulo

    def delete(self, using=None, keep_parents=False):
        self.imagen.delete(self.imagen.name)
        super().delete()

# Clase Comentario
class Comentario(models.Model):
    posts = models.ForeignKey('post.Posts', on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto
