from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import *

router = DefaultRouter()
router.register(r'internal-transfer-delivery-request', InternalTransferDeliveryRequestView) 
router.register(r'update-delivery-request', updateDeliveryRequestView) 
router.register(r'send-to-distribution', sendToDistributionView)
router.register(r'get-warehouseID', getWarehouseIDView) 
router.register(r'InternalTransferReworkOrder', InternalTransferReworkOrderView) 

# Define the URL patterns
urlpatterns = [
    path('operation/', include(router.urls)), 
]
