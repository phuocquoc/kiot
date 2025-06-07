from django.db import models

from customer.models import Customer
from product.models import Product
from user.models import User


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to="invoices/", blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.id}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.quantity * self.price_per_item
