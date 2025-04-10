from rest_framework import viewsets
from .models import *
from .serializers import *

class DeliveryReceiptView(viewsets.ModelViewSet):
    queryset = DeliveryReceiptData.objects.all()
    serializer_class = DeliveryReceiptSerializer

class BillingReceiptView(viewsets.ModelViewSet):
    queryset = BillingReceiptData.objects.all()
    serializer_class = BillingReceiptSerializer

class DeliveryReworkOrderView(viewsets.ModelViewSet):
    queryset = DeliveryReworkOrderData.objects.all()
    serializer_class = DeliveryReworkOrderSerializer