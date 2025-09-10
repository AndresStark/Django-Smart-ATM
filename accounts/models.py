from django.contrib.auth.models import AbstractUser

from django.db import models


"""

Model: UserATM (User Automatic Teller Machine)
Customized User model so it can store the user personal data, neccesary for bank data.
* has_account = Verification if the user has already created an account

"""
class UserATM(AbstractUser):
    first_name = models.CharField(blank=True, max_length=200, verbose_name="first_name")
    last_name = models.CharField(blank=True, max_length=200, verbose_name="last_name")
    phone = models.CharField(max_length=20, null=True, verbose_name="phone")
    address = models.CharField(max_length=500, null=True, verbose_name="address")
    email = models.EmailField(blank=True, max_length=100, verbose_name="email")
    birth_date = models.DateField(null=True, verbose_name="birth_date")
    has_account = models.BooleanField(default=False, verbose_name="has_account")


"""

Model: Account
Core model that manages the registers for the user's stored balances.
* account_number = Identificator for the account, it will be used to make transactions
* balance = Amount of money stored in the account
* account_authenticated = When created, it is asked for the password of the user. It verifies that.
"""
class Account(models.Model):
    user = models.ForeignKey(UserATM, on_delete=models.CASCADE, verbose_name="user")
    account_number = models.CharField(null=True, verbose_name="account_number")
    balance = models.FloatField(default=0, verbose_name="balance")
    account_authenticated = models.BooleanField(default=False, verbose_name="account_authenticated")

    def __str__(self):
        if not self.account_number == None:
            return f"My account number: {self.account_number}"
        else:
            return "Account damaged"


"""

Model: Machine Account
Admin type of account, only accessed by admins. Represents the physical bills of each ATM.
It is thought to be able to store different currencies at once, as a centralized system.
* machine_mac = Identifier for the physical ATM
* machine_ip = Network identifier for the ATM. Not used in this project, but included as good practices
"""
class MachineAccount(Account):
    machine_mac = models.CharField(max_length=15, verbose_name="machine_mac")
    machine_ip = models.CharField(max_length=12, verbose_name="machine_ip")
    
    def __str__(self):
        if not self.account_number == None:
            return f"Machine Account Number: {self.account_number}"
        else:
            return "Account damaged"