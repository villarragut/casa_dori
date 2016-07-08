from django.db import models
from django.utils import timezone


class Reservation(models.Model):
    name = models.CharField(max_length=64,
                            verbose_name="Nombre y apellidos")
    dni = models.CharField(max_length=64,
                           verbose_name="D.N.I. o pasaporte")
    email = models.CharField(max_length=64,
                             verbose_name="Correo electrónico")
    phone = models.CharField(max_length=64,
                             verbose_name="Número de teléfono")
    initial_date = models.DateField(verbose_name="Fecha de entrada")
    final_date = models.DateField(verbose_name="Fecha de salida")
    reservation_date = models.DateTimeField(default=timezone.now,
                                            verbose_name="Fecha y hora de reserva")
    reference = models.CharField(max_length=8,
                                 verbose_name="Localizador")
    confirmation_date = models.DateTimeField(blank=True, # django
                                             null=True, # db
                                             verbose_name="Fecha y hora de confirmación")
    deposit = models.BooleanField(default=False,
                                  verbose_name="Fianza pagada")
    invoice = models.BooleanField(default=False,
                                  verbose_name="Factura final pagada")
    
    class Meta:
        ordering = ["initial_date"]
        verbose_name = "reserva"
        verbose_name_plural = "reservas"

    def __str__(self):
        return "{0} → {1}".format(self.initial_date, self.final_date)
    
