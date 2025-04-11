from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'vendors', VendorDataViewSet)  # /api/vendors/
router.register(r'employee', EmployeeDataViewSet)  # /api/employee/
urlpatterns = [
    path("operation/", include(router.urls)),  # Base API path for viewsets
    path("operation/supplier/", SupplierView.as_view(), name="supplier-data"),  # Custom APIView path

]
