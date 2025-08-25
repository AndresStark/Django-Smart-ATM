from django.contrib.auth.models import AbstractUser

from django.db import models


class UserATM(AbstractUser):
    first_name = models.CharField(blank=True, max_length=200, verbose_name="nombre")
    last_name = models.CharField(blank=True, max_length=200, verbose_name="apellido")
    phone = models.CharField(max_length=20, null=True, verbose_name="telefono")
    address = models.CharField(max_length=500, null=True, verbose_name="direccion")
    email = models.EmailField(blank=True, max_length=100, verbose_name="email")
    birth_date = models.DateField(null=True, verbose_name="fecha_de_nacimiento")
    has_account = models.BooleanField(default=False, verbose_name="tiene_cuenta")

class Account(models.Model):
    user = models.ForeignKey(UserATM, on_delete=models.CASCADE, verbose_name="usuario")
    account_number = models.CharField(null=True, verbose_name="numero_de_cuenta")
    balance = models.FloatField(default=0, verbose_name="balance")
    account_authenticated = models.BooleanField(default=False, verbose_name="cuenta_autenticada")

    def __str__(self):
        if not self.account_number == None:
            return f"Mi número de cuenta: {self.account_number}"
        else:
            return "Cuenta dañada"