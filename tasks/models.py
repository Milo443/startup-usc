from django.db import models

# Create your models here.

class Usuario(models.Model):
        nombre = models.CharField(max_length=50)
        apellido = models.CharField(max_length=50)
        email = models.EmailField(max_length=50)
        password = models.CharField(max_length=50)
        def __str__(self):
                return self.nombre
        
class Startup(models.Model):
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=50, verbose_name='Nombre del proyecto')
        descripcion = models.CharField(max_length=50, verbose_name='Descripcion del proyecto')
        categoria = models.CharField(max_length=50, verbose_name='Categoria del proyecto')
        imagen = models.ImageField(upload_to='startup_images/', verbose_name='Imagen del proyecto')
        username = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')
        def __str__(self):
                return self.nombre
        
class Libros(models.Model):
        id = models.AutoField(primary_key=True)
        titulo = models.CharField(max_length=50, verbose_name='Titulo del libro')
        autor = models.CharField(max_length=50, verbose_name='Autor del libro')
        editorial = models.CharField(max_length=50, verbose_name='Editorial del libro')
        imagen = models.ImageField(upload_to='libros_images/', verbose_name='Imagen del libro')
        def __str__(self):
                return self.titulo