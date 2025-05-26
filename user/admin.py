from django.contrib import admin

from .models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)

class UserInline(admin.TabularInline):
    model = User
    extra = 0

@admin.register(User)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['*']
    inlines = [UserInline]
    readonly_fields = ['total_amount', 'created_at']
