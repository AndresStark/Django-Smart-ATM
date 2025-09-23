import math

from django.shortcuts import redirect

from django.views import generic
from django.urls import reverse_lazy, reverse
from django.forms import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import UserATM, Account, MachineAccount

from .models import Transaction, TransactionBills, MachineAccountBills
from .choices import TRANSACTION_STATUS, TRANSACTION_TYPE
from .forms import WithdrawTransactionForm, DepositTransactionForm, TransferTransactionForm, TransactionVerificationForm



class WithdrawTransactionFormView(LoginRequiredMixin, generic.FormView):
    form_class = WithdrawTransactionForm
    template_name = 'transactions/withdraw.html'
    success_url = reverse_lazy('transactions:verification')
    
    """
    Creates Transaction type Withdraw in status On Going, and saves it in the database
    """
    def form_valid(self, form):
        user = UserATM.objects.get(username=self.request.user.username)
        account = Account.objects.get(user=user)
        machine_account = MachineAccount.objects.last() #Provisional status. Should be able to select session's machine
        print(f"My user: {user}, {account}")
        form.instance.origin_account = account
        form.instance.machine_transactor = machine_account
        form.instance.transaction_type = TRANSACTION_TYPE['W']
        form.instance.status = TRANSACTION_STATUS[2]
        form.instance.amount = abs(form.cleaned_data['amount'])
        form.save()
        return super().form_valid(form)

class DepositTransactionFormView(LoginRequiredMixin, generic.FormView):
    form_class = DepositTransactionForm
    template_name = 'transactions/deposit.html'
    success_url = reverse_lazy('transactions:verification')
    
    """
    Creates Transaction type Deposite in status On Going, and saves it in the database
    """
    def form_valid(self, form):
        user = UserATM.objects.get(username=self.request.user.username)
        account = Account.objects.get(user=user)
        machine_account = MachineAccount.objects.last() #Provisional status. Should be able to select session's machine
        print(f"My user: {user}, {account}")
        form.instance.origin_account = account
        form.instance.machine_transactor = machine_account
        form.instance.transaction_type = TRANSACTION_TYPE['D']
        form.instance.status = TRANSACTION_STATUS[2]
        form.instance.amount = abs(form.cleaned_data['amount'])
        form.save()
        return super().form_valid(form)

class TransferTransactionFormView(LoginRequiredMixin, generic.FormView):
    form_class = TransferTransactionForm
    template_name = 'transactions/transfer.html'
    success_url = reverse_lazy('transactions:verification')
    
    """
    Creates Transaction type Transfer in status On Going, and saves it in the database
    """
    def form_valid(self, form):
        user = UserATM.objects.get(username=self.request.user.username)
        account = Account.objects.get(user=user)
        machine_account = MachineAccount.objects.last() #Provisional status. Should be able to select session's machine
        print(f"My user: {user}, {account}")
        form.instance.origin_account = account
        form.instance.machine_transactor = machine_account
        form.instance.destiny_account_number = form.cleaned_data['destiny_account_number']
        form.instance.transaction_type = TRANSACTION_TYPE['T']
        form.instance.status = TRANSACTION_STATUS[2]
        form.instance.amount = abs(form.cleaned_data['amount'])
        form.save()
        return super().form_valid(form)

class TransactionVerificationView(LoginRequiredMixin, generic.FormView):
    form_class = TransactionVerificationForm
    template_name = 'status/verification.html'
    success_url = reverse_lazy('transactions:success')
    
    """
    Given the current transaction's amount, calculates the respective amount and types of bills required.
    """
    def calculate_bills(self, transaction: Transaction):
        transaction_bills = list(TransactionBills.objects.filter(transaction=transaction))
        if len(transaction_bills) > 0:
            print("Bills already exist")
            return
        
        requested_money = transaction.amount
        temporal_bills: dict[str, TransactionBills] = {}
        box_bills: dict[str, MachineAccountBills] = {}
        box = list(MachineAccountBills.objects.filter(machine_account=transaction.machine_transactor).order_by('bill').reverse())
        print(box_bills)
        for box_bill in box:
            box_bills[str(box_bill.bill.value)] = box_bill

        for clave in box_bills.keys():
            print(clave)
            stored_bill = box_bills[clave]

            current_bill = TransactionBills()
            current_bill.bill = stored_bill.bill
            current_bill.transaction = transaction

            if requested_money > 0:
                division = math.floor(requested_money / stored_bill.bill.value)
                if division > stored_bill.quantity:
                    current_bill.quantity = stored_bill.quantity
                else:
                    current_bill.quantity = division
                
                temporal_bills[clave] = current_bill
                print(f'Transaction bills: {temporal_bills[clave].bill}')
                print(f'Current bill: {current_bill.bill} * {current_bill.quantity}')
                print("")
                requested_money -= current_bill.sum_value()

                if requested_money <= 0:
                    print("Here machine bills are reduced")

        if requested_money == 0:
            for bill in temporal_bills.values():
                print(f'Transaction final bills: {bill.bill} * {bill.quantity}')
                if bill.quantity != 0:
                    bill.save()
            return 1
        elif requested_money >= 1:
            print("Not enough cash in the machine")
            print(requested_money)
            return 0
        elif requested_money > 0 and requested_money < 1:
            print("Decimals were used")
            print(requested_money)
            return 0
        else:
            print("Failed bill calculation")
            print(requested_money)
            return 0

    """
    Given the current transaction, discounts the quantity of bills used in the transaction from the machine
    """
    def discount_bills(self, transaction: Transaction):
        transaction_bills_dict: dict[str, TransactionBills] = {}
        machine_bills_dict: dict[str, MachineAccountBills] = {}

        transaction_bills = list(TransactionBills.objects.filter(transaction=transaction).order_by('bill').reverse())
        machine_bills = list(MachineAccountBills.objects.filter(machine_account=transaction.machine_transactor).order_by('bill').reverse())

        for bill in transaction_bills:
            transaction_bills_dict[str(bill.bill.value)] = bill
            
        for bill in machine_bills:
            machine_bills_dict[str(bill.bill.value)] = bill

        for value in transaction_bills_dict.keys():
            machine_bills_dict[value].quantity -= transaction_bills_dict[value].quantity
            machine_bills_dict[value].save()

    
    """
    Verifies the current user's last On Going transaction with password, and adds
    the amount to the user's Account balance
    """
    def form_valid(self, form: TransactionVerificationForm):
        user = UserATM.objects.get(username=self.request.user.username)
        account = Account.objects.get(user=user)
        transaction: Transaction = Transaction.objects.filter(origin_account=account, status="On going").last()
        
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
                if transaction.origin_account.balance >= transaction.amount:
                    print(f'The transaction data is: {transaction}')
                    calculation = self.calculate_bills(transaction)
                    if calculation == 1:
                        check_transaction = True
                        self.discount_bills(transaction)
                        account.balance = account.balance - transaction.amount
                        account.save()
            
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
                if transaction.origin_account.balance >= transaction.amount:
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
                transaction.status = "Failed"
                return redirect(reverse_lazy('transactions:failed'))

        # If password was incorrect:
        else:
            ValidationError('Incorrect password')
        return super().form_valid(form)

class TransactionSuccessView(LoginRequiredMixin, generic.DetailView):
    model = Transaction
    template_name = "status/success.html"
    context_object_name = "queryset"

    def get_object(self, queryset = None):
        user = UserATM.objects.get(username=self.request.user.username)
        account = Account.objects.get(user=user)
        transaction: Transaction = Transaction.objects.filter(origin_account=account, status="Successful").last()

        print(transaction.status)
        print(transaction.transaction_type)
        print(type(transaction.transaction_type))
        
        if transaction.transaction_type == "withdraw":
            transaction_bills = list(TransactionBills.objects.filter(transaction=transaction))
            printed_bills = []
            for bill in transaction_bills:
                for _ in range(bill.quantity):
                    printed_bills.append(bill.bill)
            queryset = {
                'transaction': transaction,
                'transaction_bills': transaction_bills,
                'printed_bills': printed_bills,
            }
        else:
            queryset = {
                'transaction': transaction,
            }
        return queryset

class TransactionFailedView(LoginRequiredMixin, generic.TemplateView):
    template_name = "status/failed.html"
