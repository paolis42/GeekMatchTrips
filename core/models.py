from django.db import models
from django.utils import timezone


class Registro(models.Model):
    nombre_lugar = models.CharField(max_length=150)
    nivel_interes = models.IntegerField()
    precio = models.IntegerField()
    presupuesto = models.IntegerField()
    resultado = models.CharField(max_length=100)
    motivo = models.CharField(max_length=300)

    fecha = models.DateTimeField(default=timezone.now)

    # Borrado lógico
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.nombre_lugar} - {self.resultado}"

    def soft_delete(self):
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save()

