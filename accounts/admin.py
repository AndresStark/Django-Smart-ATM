from django.contrib import admin

from .models import UserATM, Account, MachineAccount

from transactions.models import MachineAccountBills

class UserATMAdmin(admin.ModelAdmin):
    model = UserATM
    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        ]
    search_fields = [
        'first_name',
        'last_name',
        ]

class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = [
        'user',
        'account_number',
        'balance',
        'account_authenticated',
    ]
    search_fields = [
        'user',
        'account_number'
    ]

class MachineAccountBillsInLineAdmin(admin.TabularInline):
    model = MachineAccountBills
    extra = 0

class MachineAccountAdmin(admin.ModelAdmin):
    model = MachineAccount
    list_display = [
        'account_number',
        'user',
        'balance',
        'account_authenticated',
        'machine_mac',
        'machine_ip',
    ]
    search_fields = [
        'user',
        'account_number'
    ]
    inlines = [
        MachineAccountBillsInLineAdmin
    ]

    """
    Method that recalculates the machine account's total balance for every bill each time called 
    """
    def update_machine_account_balance(self, machine_account):
        total = 0
        value = 0
        bills = MachineAccountBills.objects.filter(machine_account=machine_account)
        
        for bill in bills:
            value = float(bill.quantity * bill.bill.value)
            total = total + value
        machine_account.balance = total
        machine_account.save()
    
    """
    Rewrited save_related method that updates the account's balance when its relatives (Bills) are saved
    """
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        account = form.instance
        self.update_machine_account_balance(account)

admin.site.register(UserATM,UserATMAdmin)
admin.site.register(Account,AccountAdmin)
admin.site.register(MachineAccount,MachineAccountAdmin)