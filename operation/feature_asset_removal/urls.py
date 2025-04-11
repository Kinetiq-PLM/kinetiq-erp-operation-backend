from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import *


router = DefaultRouter()
router.register(r'item-removal', AssetRemovalView) 
router.register(r'send-to-management', sendToManagementView) 

# Define the URL patterns
urlpatterns = [
    path('operation/', include(router.urls)), 
]

