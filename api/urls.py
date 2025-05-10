# from django.urls import include, path
# from rest_framework import routers
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#
# from .views import CustomerViewSet, InvoiceViewSet, ProductViewSet, StockHistoryViewSet
#
# router = routers.DefaultRouter()
# router.register(r"products", ProductViewSet)
# router.register(r"customers", CustomerViewSet)
# router.register(r"invoices", InvoiceViewSet)
# router.register(r"stocks", StockHistoryViewSet)
#
# urlpatterns = [
#     path("", include(router.urls)),
#     path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
# ]
