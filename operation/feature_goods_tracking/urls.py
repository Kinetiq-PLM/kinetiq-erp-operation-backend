from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (GoodsTrackingDataViewSet, get_next_document_info, DocumentItemsViewSet, 
                     get_item_options, createDocumentItem, SalesInvoiceView)

router = DefaultRouter()
router.register(r'goods-tracking', GoodsTrackingDataViewSet)
router.register(r'document-item', DocumentItemsViewSet, basename='document-item-view') 
router.register(r'create-items', createDocumentItem, basename='create-items')
router.register(r'sales-invoice', SalesInvoiceView)
urlpatterns = [
    path("operation/", include(router.urls)),  # Base API path for viewsets
    path('operation/next-document-info/', get_next_document_info, name='next-document-info'),
    path('operation/get-item-options/', get_item_options, name='get-item-options'),
]
