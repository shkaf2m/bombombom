from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from bankapp.models import CustomUser, MoneyOrder
from bankapp.forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.

admin.site.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    # list_display = UserAdmin.list_display + ('course', 'money', 'account_number')
    list_display = ('username', 'first_name', 'last_name', 'email', 'course', 'money', 'account_number')

admin.site.register(MoneyOrder)
class MoneyOrderAdmin(admin.ModelAdmin):
    list_display = ['sender_username', 'recipient_username', 'money_sum']