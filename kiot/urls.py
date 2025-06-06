from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from customer.views import CustomerViewSet
from invoice.views import InvoiceViewSet
from product.views import ProductViewSet
from stock.views import StockHistoryViewSet
from django.urls import path
from django.shortcuts import render

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"invoices", InvoiceViewSet)
router.register(r"stocks", StockHistoryViewSet)

urlpatterns = [
    # path('', lambda request: render(request, "index.html")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),  # Gọi API routes
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
