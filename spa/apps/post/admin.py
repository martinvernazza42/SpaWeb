from django.contrib import admin
from .models import Categoria, Posts, User, Comentario


# Register your models here.

@admin.register (Posts)
class PostsAdmin (admin.ModelAdmin):
    list_display = ('id','titulo','subtitulo','fecha','texto','activo','categoria','imagen','publicado')
    

admin.site.register (Categoria) 
