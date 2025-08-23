from django.contrib import admin

from .models import UserATM, Account

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

admin.site.register(UserATM,UserATMAdmin)
admin.site.register(Account,AccountAdmin)