from django.shortcuts import redirect

from django.views import generic
from django.urls import reverse_lazy, reverse
from django.forms import ValidationError

from accounts.models import UserATM, Account

from .models import Transaction
from .choices import TRANSACTION_STATUS, TRANSACTION_TYPE
from .forms import WithdrawTransactionForm, DepositTransactionForm, TransferTransactionForm, TransactionVerificationForm



class WithdrawTransactionFormView(generic.FormView):
    form_class = WithdrawTransactionForm
    template_name = 'transactions/withdraw.html'
    success_url = reverse_lazy('transactions:verification')
    
    """
    Creates Transaction type Withdraw in status On Going, and saves it in the database
    """
    def form_valid(self, form):
        user = UserATM.objects.get(username=self.request.user.username)
        account = Account.objects.get(user=user)
        print(f"My user: {user}, {account}")
        form.instance.origin_account = account
        form.instance.transaction_type = TRANSACTION_TYPE['W']
        form.instance.status = TRANSACTION_STATUS[2]
        form.instance.amount = abs(form.cleaned_data['amount'])
        form.save()
        return super().form_valid(form)

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
        form.instance.amount = abs(form.cleaned_data['amount'])
        form.save()
        return super().form_valid(form)

class TransferTransactionFormView(generic.FormView):
    form_class = TransferTransactionForm
    template_name = 'transactions/transfer.html'
    success_url = reverse_lazy('transactions:verification')
    
    """
    Creates Transaction type Transfer in status On Going, and saves it in the database
    """
    def form_valid(self, form):
        user = UserATM.objects.get(username=self.request.user.username)
        account = Account.objects.get(user=user)
        print(f"My user: {user}, {account}")
        form.instance.origin_account = account
        form.instance.destiny_account_number = form.cleaned_data['destiny_account_number']
        form.instance.transaction_type = TRANSACTION_TYPE['T']
        form.instance.status = TRANSACTION_STATUS[2]
        form.instance.amount = abs(form.cleaned_data['amount'])
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
        
        # Verifies the password for the current user
        if user.check_password(form.obtain_password()):
            check_transaction = False

            if transaction.transaction_type == TRANSACTION_TYPE['W']:
                """
                Withdraw Transaction
                """
                check_transaction = True
                account.balance = account.balance - transaction.amount
                account.save()
                print("Billetes")
            
            elif transaction.transaction_type == TRANSACTION_TYPE['D']:
                """
                Deposit Transaction
                """
                check_transaction = True
                account.balance = account.balance + transaction.amount
                account.save()
                
            elif transaction.transaction_type == TRANSACTION_TYPE['T']:
                """
                Transfer Transaction
                """
                destiny_account = Account.objects.get(account_number=transaction.destiny_account_number)
                print(destiny_account)
                if isinstance(destiny_account, Account):
                    check_transaction = True
                    account.balance = account.balance - transaction.amount
                    account.save()
                    destiny_account.balance = destiny_account.balance + transaction.amount
                    destiny_account.save()
                else:
                    return redirect(reverse_lazy('transactions:failed'))
            
            elif transaction.transaction_type == TRANSACTION_TYPE['N'] or transaction.transaction_type == None:
                """
                Failed Transaction
                """
                return redirect(reverse_lazy('transactions:failed'))

            # Checks if transaction was processed correctly
            if check_transaction:
                transaction.status = "Successful"
                transaction.save()
            else:
                return redirect(reverse_lazy('transactions:failed'))

        # If password was incorrect:
        else:
            ValidationError('Incorrect password')
        return super().form_valid(form)

class TransactionSuccessView(generic.TemplateView):
    template_name = "status/success.html"

class TransactionFailedView(generic.TemplateView):
    template_name = "status/failed.html"
