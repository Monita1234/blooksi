from django.contrib import admin
from biblioteca.apps.libros.models import *

admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Categoria)
admin.site.register(Libro)
admin.site.register(Biblioteca)
admin.site.register(Usuario)
admin.site.register(Bibliotecario)
admin.site.register(Prestamo)
admin.site.register(Tipo_Usuario)
admin.site.register(Ciudad)
admin.site.register(Busqueda)