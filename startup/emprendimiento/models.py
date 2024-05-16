from django.db import models

# Create your models here.

class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.nombre
    
class Financiero(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    ventas = models.FloatField(null=True, blank=True)
    costos_produccion = models.FloatField(null=True, blank=True)
    gastos_administrativos = models.FloatField(null=True, blank=True)
    capital_propio = models.FloatField(null=True, blank=True)
    prestamo = models.FloatField(null=True, blank=True)
    inversores = models.FloatField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.proyecto.nombre