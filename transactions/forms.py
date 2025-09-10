from django import forms

from .models import Transaction
from .choices import BILLS_CURRENCIES, BILLS_USD


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = []


class DepositTransactionForm(TransactionForm):
    amount = forms.FloatField(label="Amount to Deposit", required=True)
    description = forms.CharField(max_length=500, label="Deposit description", required=False)


class TransferTransactionForm(TransactionForm):
    destiny_account_number = forms.CharField(max_length=16, label="Destiny Account Number", required=True)
    amount = forms.FloatField(label="Amount to Transfer", required=True)
    description = forms.CharField(max_length=500, label="Transfer description")


class WithdrawTransactionForm(TransactionForm):
    amount = forms.FloatField(label="Amount to Deposit", required=True)
    description = forms.CharField(max_length=500, label="Withdraw description")


class TransactionVerificationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Current Password", required=True)

    def obtain_password(self):
        return self.cleaned_data['password']