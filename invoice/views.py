from django.shortcuts import render
from rest_framework import viewsets

from invoice.models import Invoice
from invoice.serializers import InvoiceSerializer

# Create your views here.


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceSerializer
