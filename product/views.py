from django.shortcuts import render
from rest_framework import viewsets

from product.models import Product
from product.serializers import ProductSerializer


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
