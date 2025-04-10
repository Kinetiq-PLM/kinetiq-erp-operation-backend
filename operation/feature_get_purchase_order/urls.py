from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseQuotationView
router = DefaultRouter()
router.register(r'purchase_order', PurchaseQuotationView)
urlpatterns = [
    path("operation/", include(router.urls)),  # Base API path for viewsets

]