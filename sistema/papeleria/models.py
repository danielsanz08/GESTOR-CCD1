from django.db import models
from django.conf import settings
# Create your models here.
class Articulo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=50, null=False, blank=False)
    observacion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=50, null=False, blank=False, default='No establecido')
    precio = models.PositiveBigIntegerField(null=False, blank=False)
    cantidad = models.PositiveIntegerField()
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True)
    fecha_registro = models.DateField(auto_now=True)
    def __str__(self):
        return self.nombre
    def observacion_formateada(self, longitud=20):  # 'self' es necesario, longitud es opcional
        if not self.observacion:  # Usa self.observacion
            return ""
        return '\n'.join(self.observacion[i:i + longitud] for i in range(0, len(self.observacion), longitud))