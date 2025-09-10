from django.db import models

from accounts.models import Account, MachineAccount

from .choices import TRANSACTION_STATUS, TRANSACTION_TYPE


"""

Model: Bill
Register each type of bill individually to measure the quantity of each type.
It's developed this way to save bills from other countries.

"""
class Bill(models.Model):
    value = models.IntegerField(verbose_name="value")
    identity = models.CharField(max_length=30, verbose_name="identity")
    currency_code = models.CharField(max_length=10, verbose_name="currency_code")
    image = models.ImageField(blank=True, verbose_name="image")

    def __str__(self):
        return f"Bill: " + self.value


"""

Model: Transaction
Base model for every transaction, so it can exist in the same database and
share common code.

"""
class Transaction(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, unique=True, verbose_name="transaction_id")
    origin_account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="origin_account")
    destiny_account_number = models.CharField(max_length=16, null=True, verbose_name="destiny_account_number")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="creation_date")
    amount = models.FloatField(default=0, verbose_name="amount")
    transaction_type = models.TextField(choices=TRANSACTION_TYPE, default=TRANSACTION_TYPE["N"], verbose_name="transaction_type")
    status = models.CharField(choices=TRANSACTION_STATUS, default=TRANSACTION_STATUS[1], verbose_name="status")
    description = models.CharField(max_length=500, blank=True, verbose_name="description")

    def __str__(self):
        return f"Transaction #{self.id} by {self.origin_account}"


"""

Model: Transaction Bills
Registers the quantity and the type of bills for each transaction

"""
class TransactionBills(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, verbose_name="transaction")
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, verbose_name="bill")
    quantity = models.IntegerField(default=0, verbose_name="quantity")

    def __str__(self):
        return f"{self.transaction} - {self.bill.value}"
    

class MachineAccountBills(models.Model):
    machine_account = models.ForeignKey(MachineAccount, on_delete=models.CASCADE, verbose_name="machine_account")
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, verbose_name="bill")
    quantity = models.IntegerField(default=0, verbose_name="quantity")

    def __str__(self):
        return f"{self.machine_account} - {self.bill.value}"