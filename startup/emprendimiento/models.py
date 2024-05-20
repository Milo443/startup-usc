from django.db import models

# Create your models here.

class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=1000)
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
    
class Marketing(models.Model):
    mercado_objetivo= models.CharField(max_length=250, null=True, blank=True)
    segmentacion_cliente = models.CharField(max_length=250, null=True, blank=True)
    canal_marketing = models.CharField(max_length=250, null=True, blank=True)
    estrategia_precio_promocion = models.CharField(max_length=250, null=True, blank=True)
    gastos_marketing = models.FloatField(null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.proyecto.nombre
    
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=50, null=True, blank=True)
    descripcion_producto = models.TextField(max_length=1000, null=True, blank=True)
    categoria_producto = models.CharField(max_length=50, null=True, blank=True)
    ciclo_vida = models.CharField(max_length=1000, null=True, blank=True)
    costo_desarrollo = models.FloatField(null=True, blank=True)  
    costo_produccion = models.FloatField(null=True, blank=True)
    precio_venta = models.FloatField(null=True, blank=True)
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class Identidad(models.Model):
    mision = models.TextField(max_length=1000, null=True, blank=True)
    vision = models.TextField(max_length=1000, null=True, blank=True)
    valores = models.TextField(max_length=500, null=True, blank=True)
    objetivos = models.TextField(max_length=1000, null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return self.proyecto.nombre

class CargoEmpleado(models.Model):
    nombre_cargo = models.CharField(max_length=50, null=True, blank=True)
    descripcion_cargo = models.TextField(max_length=1000, null=True, blank=True)
    requisitos_cargo = models.TextField(max_length=1000, null=True, blank=True)
    salario = models.FloatField(null=True, blank=True)
    numero_empleados = models.IntegerField(null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return self.proyecto.nombre


