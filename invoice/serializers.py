from rest_framework import serializers

from customer.models import Customer
from customer.serializers import CustomerSerializer
from invoice.models import Invoice, InvoiceItem
from invoice.service import InvoiceItemService
from product.models import Product
from product.serializers import ProductSerializer
from user.models import User
from user.serializers import UserSerializer
from django.db import transaction

class InvoiceItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = InvoiceItem
        fields = ["id", "product", "quantity", "price_per_item", "total_price"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["product"] = ProductSerializer(instance.product).data
        return rep


class InvoiceSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), allow_null=True, required=False)
    staff = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = "__all__"

    def to_internal_value(self, data):
        if view := self.context.get("view"):
            data.update(staff=view.request.user.id)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["customer"] = CustomerSerializer(instance.customer).data
        rep["staff"] = UserSerializer(instance.staff).data
        return rep

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items", None)
        invoice = super().create(validated_data)
        if items:
            for item in items:
                product = item['product']
                quantity_requested = item['quantity']
                if product.stock_quantity < quantity_requested:
                    raise serializers.ValidationError(
                        f"Sản phẩm '{product.name}' không đủ tồn kho. Còn lại: {product.stock_quantity}")

            InvoiceItemService.bulk_create_invoice_item(invoice=invoice, items=items)
        return invoice
