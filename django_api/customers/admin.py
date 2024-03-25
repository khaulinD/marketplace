from django.contrib import admin

from customers.models import Account


# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ['email', "username", "first_name", "last_name", "is_active", "logo", "date_joined", "last_login"]

admin.site.register(Account, AccountAdmin)