from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseOrderView

router = DefaultRouter()
router.register(r'purchase_order', PurchaseOrderView, basename='purchase-order')

urlpatterns = [
    path("operation/", include(router.urls)),  # Base API path for viewsets
]
