from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (GoodsTrackingDataViewSet, ProductDocuItemView, get_next_document_info, DocumentItemsViewSet, 
                     get_item_options, createDocumentItem, SalesInvoiceView)

router = DefaultRouter()
router.register(r'goods-tracking', GoodsTrackingDataViewSet)  # /api/goods-tracking/
router.register(r'document-item', DocumentItemsViewSet, basename='document-item-view')  # /api/goods-tracking/
router.register(r'product-docu-item', ProductDocuItemView)  # /api/goods-tracking/ createDocumentItem
router.register(r'create-items', createDocumentItem, basename='create-items')
router.register(r'sales-invoice', SalesInvoiceView)
urlpatterns = [
    path("operation/", include(router.urls)),  # Base API path for viewsets
    path('operation/next-document-info/', get_next_document_info, name='next-document-info'),
    path('operation/get-item-options/', get_item_options, name='get-item-options'),
]
