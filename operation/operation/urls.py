from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from feature_asset_removal.urls import router as asset_removal_router
from feature_delivery_receipt.urls import router as delivery_receipt_router
from feature_get_purchase_order.urls import router as purchase_order_router
from feature_get_reference_data.urls import router as reference_router
from feature_goods_tracking.urls import router as goods_tracking_router
from feature_internal_transfer.urls import router as internal_transfer_router
from feature_update_delivery_approval.urls import router as update_delivery_approval

admin_router = DefaultRouter()
admin_router.registry.extend(asset_removal_router.registry)
admin_router.registry.extend(delivery_receipt_router.registry)
admin_router.registry.extend(purchase_order_router.registry)
admin_router.registry.extend(reference_router.registry)
admin_router.registry.extend(goods_tracking_router.registry)
admin_router.registry.extend(internal_transfer_router.registry)
admin_router.registry.extend(update_delivery_approval.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("feature_asset_removal.urls")),
    path("", include("feature_delivery_receipt.urls")),
    path("", include("feature_get_purchase_order.urls")),
    path("", include("feature_get_reference_data.urls")),
    path("", include("feature_goods_tracking.urls")),
    path("", include("feature_internal_transfer.urls")),
    path("", include("feature_update_delivery_approval.urls")),

]