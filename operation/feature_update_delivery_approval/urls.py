from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import *




router = DefaultRouter()
router.register(r'update-delivery-approval', updateDeliveryApprovalView) 
router.register(r'delivery-approval', DeliveryApprovalView)


# Define the URL patterns
urlpatterns = [
    path('operation/', include(router.urls)), 
]
