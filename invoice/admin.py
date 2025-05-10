from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'staff', 'total_amount', 'created_at']
    inlines = [InvoiceItemInline]
    readonly_fields = ['total_amount', 'created_at']
