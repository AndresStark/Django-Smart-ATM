from django.contrib import admin

from .models import Bill, Transaction, TransactionBills

class BillAdmin(admin.ModelAdmin):
    model = Bill
    list_display = [
        'identity',
        'value',
        'currency_code',
        'image',
    ]
    search_fields = [
        'value',
        'currency_code',
    ]

class TransactionBillsInLineAdmin(admin.TabularInline):
    model = TransactionBills
    extra = 0

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = [
        'id',
        'origin_account',
        'destiny_account_number',
        'machine_transactor',
        'creation_date',
        'amount',
        'transaction_type',
        'status',
        'description',
    ]
    inlines = [
        TransactionBillsInLineAdmin
    ]

admin.site.register(Bill, BillAdmin)
admin.site.register(Transaction, TransactionAdmin)