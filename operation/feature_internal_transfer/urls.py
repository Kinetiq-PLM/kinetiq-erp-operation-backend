from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import *

router = DefaultRouter()
router.register(r'InternalTransferDeliveryRequest', InternalTransferDeliveryRequestView) 
router.register(r'updateDRWarehouse', updateDRWarehouseView) 
router.register(r'getWarehouseID', getWarehouseIDView) 
router.register(r'InternalTransferReworkOrder', InternalTransferReworkOrderView) 

# Define the URL patterns
urlpatterns = [
    path('operation/', include(router.urls)), 
]
