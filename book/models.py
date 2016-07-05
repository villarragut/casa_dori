from django.db import models
from django.utils import timezone


class Reservation(models.Model):
    author = models.ForeignKey('auth.User')
    name = models.CharField(max_length=200)
    dni = models.CharField(max_length=10)
    initial_date = models.DateField()
    final_date = models.DateField()
    reservation_date = models.DateTimeField(default=timezone.now)
    confirmation_date = models.DateTimeField(blank=True, null=True)
    deposit = models.BooleanField(default=False)
    invoice = models.BooleanField(default=False)

    def confirm(self):
        self.confirmation_date = timezone.now()
        self.save()
    
    def pay_deposit(self):
        self.deposit = True
        self.save()
        
    def pay_invoice(self):
        self.invoice = True
        self.save()

    def __str__(self):
        return "{0} → {1}".format(self.initial_date, self.final_date)
    
