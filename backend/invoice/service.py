from invoice.models import Invoice, InvoiceItem
from product.models import Product


class InvoiceItemService:

    @classmethod
    def bulk_create_invoice_item(cls, invoice: Invoice, items: dict):
        invoice_items = []
        products = []
        for item in items:
            invoice_items.append(InvoiceItem(invoice=invoice, **item))
            product = item["product"]
            product.stock_quantity -= item["quantity"]
            products.append(product)
        Product.objects.bulk_update(products, fields=["stock_quantity"])
        InvoiceItem.objects.bulk_create(invoice_items)
