from django.db import models

from django.contrib.auth.models import User

class UserATM(User):
    # first_name = models.CharField(default="", max_length=200, verbose_name="nombres")
    # last_name = models.CharField(default="", max_length=200, verbose_name="apellidos")
    phone = models.CharField(max_length=20, null=True, verbose_name="telefono")
    address = models.CharField(max_length=500, null=True, verbose_name="direccion")
    # email = models.EmailField(null=True, max_length=100, verbose_name="email")
    birth_date = models.DateField(null=True, verbose_name="fecha_de_nacimiento")

class Account(models.Model):
    user = models.ForeignKey(UserATM, on_delete=models.CASCADE, null=True, verbose_name="usuario")
    account_number = models.CharField(null=True, verbose_name="numero_de_cuenta")
    balance = models.FloatField(default=0, verbose_name="balance")
    account_authenticated = models.BooleanField(default=False, verbose_name="cuenta_autenticada")

    def __str__(self):
        return f"{self.user.first_name}: " + self.account_number