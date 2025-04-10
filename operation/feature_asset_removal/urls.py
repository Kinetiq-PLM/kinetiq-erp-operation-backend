from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import *


router = DefaultRouter()
router.register(r'AssetRemoval', AssetRemovalView) 
router.register(r'sendToManagement', sendToManagementView) 

# Define the URL patterns
urlpatterns = [
    path('operation/', include(router.urls)), 
]

