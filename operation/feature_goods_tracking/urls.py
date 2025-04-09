from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorDataViewSet, EmployeeDataViewSet, GoodsTrackingDataViewSet, SupplierView, ProductDocuItemView, get_next_document_info, DocumentItemsViewSet

router = DefaultRouter()
router.register(r'vendors', VendorDataViewSet)  # /api/vendors/
router.register(r'employee', EmployeeDataViewSet)  # /api/employee/
router.register(r'goods-tracking', GoodsTrackingDataViewSet)  # /api/goods-tracking/
router.register(r'document-item', DocumentItemsViewSet, basename='document-item-view')  # /api/goods-tracking/
router.register(r'product-docu-item', ProductDocuItemView)  # /api/goods-tracking/
urlpatterns = [
    path("operation/", include(router.urls)),  # Base API path for viewsets
    path("operation/supplier/", SupplierView.as_view(), name="supplier-data"),  # Custom APIView path
    path('operation/next-document-info/', get_next_document_info, name='next-document-info'),

]
