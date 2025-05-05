from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import *

router = DefaultRouter()
router.register(r'DeliveryReturnOrder', DeliveryReworkOrderView) 
router.register(r'DeliveryReceipt', DeliveryReceiptView) 
router.register(r'BillingReceipt', BillingReceiptView) 
router.register(r'GoodsIssue', ExternalGoodsIssueView) 


# Define the URL patterns
urlpatterns = [
    path('operation/', include(router.urls)), 
]
