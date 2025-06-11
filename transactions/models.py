from django.db import models


"""

Modelo: Billetes
Registra cada billete individualmente. Está pensado para almacenar también
billetes de otros países

"""
class Bill(models.Model):
    value = models.IntegerField(verbose_name="valor")
    identity = models.TextField(max_length=30, verbose_name="identidad")
    # image = models.ImageField(upload_to="static/imgs", null=True, blank=True, verbose_name="imagen")
    
    # Para futuras actualizaciones: Registros individuales para billetes
    # serial_number = models.TextField(max_length=100, verbose_name="numero_de_serie")

    def __str__(self):
        return f"Billete de " + self.value


"""

Modelo: Transacciones
Registra cada movimiento de dinero: Retiro, depósito y transferencia

"""
class Transaction(models.Model):
    TRANSACTION_TYPE = [
        "withdraw",
        "deposit",
        "transfer",
    ]

    creation_date = models.DateTimeField(null=True, auto_created=True, verbose_name="fecha_de_creacion")
    sum = models.IntegerField(verbose_name="monto")
    # transaction_type = models.TextField(choices=TRANSACTION_TYPE, verbose_name="tipo_de_transaccion")
    status = models.CharField(max_length=100, default="On going", verbose_name="estado")
    bills = models.ForeignKey(Bill, on_delete=models.PROTECT, verbose_name="billetes")
    
    # Para futuras actualizaciones: Sistema de Login para cuentas de banco
    
    def __str__(self):
        return f"Transaction {self.id} by ACCOUNT"


"""

Modelo: Billetes de Transacción
Registra los billetes utilizados en X transacciones

"""
class TransactionBills(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, verbose_name="transaccion")
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, verbose_name="billete")
    quantity = models.IntegerField(null=True, verbose_name="cantidad")

    def __str__(self):
        return f"{self.transaction} - {self.bill}"