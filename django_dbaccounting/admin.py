from django.contrib import admin

from .models import AccountType,Account,Transaction
# Register your models here.

admin.site.register(AccountType)
admin.site.register(Account)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ['date','from_acc','to_acc']