from rest_framework import serializers

from product.serializers import ProductSerializer
from stock.models import StockHistory


class StockHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = StockHistory
        fields = "__all__"
