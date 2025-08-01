from rest_framework import viewsets
from .models import PurchaseOrderData
from .serializers import PurchaseOrderSerializer

class PurchaseOrderView(viewsets.ReadOnlyModelViewSet):  
    queryset = PurchaseOrderData.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'purchase_id'
