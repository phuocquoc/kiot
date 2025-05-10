from django.shortcuts import render
from rest_framework import viewsets

from stock.models import StockHistory
from stock.serializers import StockHistorySerializer


# Create your views here.
class StockHistoryViewSet(viewsets.ModelViewSet):
    queryset = StockHistory.objects.all()
    serializer_class = StockHistorySerializer
