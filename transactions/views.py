from django.shortcuts import redirect

from django.views import generic
from django.urls import reverse_lazy, reverse
from django.forms import ValidationError

from accounts.models import UserATM, Account

from .models import Transaction
from .choices import TRANSACTION_STATUS, TRANSACTION_TYPE
from .forms import DepositTransactionForm, TransferTransactionForm, WithdrawTransactionForm, TransactionVerificationForm



class DepositTransactionFormView(generic.FormView):
    form_class = DepositTransactionForm
    template_name = 'transactions/deposit.html'
    success_url = reverse_lazy('transactions:verification')
    
    """
    Creates Transaction type Deposite in status On Going, and saves it in the database
    """
    def form_valid(self, form):
        user = UserATM.objects.get(username=self.request.user.username)
        account = Account.objects.get(user=user)
        print(f"My user: {user}, {account}")
        form.instance.origin_account = account
        form.instance.transaction_type = TRANSACTION_TYPE['D']
        form.instance.status = TRANSACTION_STATUS[2]
        form.instance.amount = form.cleaned_data['amount']
        form.save()
        return super().form_valid(form)

class TransactionVerificationView(generic.FormView):
    form_class = TransactionVerificationForm
    template_name = 'status/verification.html'
    success_url = reverse_lazy('transactions:success')
    
    """
    Verifies the current user's last On Going transaction with password, and adds
    the amount to the user's Account balance
    """
    def form_valid(self, form: TransactionVerificationForm):
        user = UserATM.objects.get(username=self.request.user.username)
        account = Account.objects.get(user=user)
        transaction: Transaction = Transaction.objects.filter(origin_account=account).last()
        print(transaction.status)
        print(transaction.transaction_type)
        if transaction == None:
            return redirect(reverse_lazy('transactions:failed'))
        if transaction.status != TRANSACTION_STATUS[2]:
            return redirect(reverse_lazy('transactions:failed'))
        if user.check_password(form.obtain_password()):
            transaction.status = "Successful"
            transaction.save()
            account.balance = account.balance + transaction.amount
            account.save()
            print(transaction.status)
            print(transaction.transaction_type)
        else:
            ValidationError('Incorrect password')
        return super().form_valid(form)


class TransactionFailedView(generic.TemplateView):
    template_name = "status/failed.html"

class TransactionSuccessView(generic.TemplateView):
    template_name = "status/success.html"