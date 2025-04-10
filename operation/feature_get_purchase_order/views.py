# views.py
from rest_framework import viewsets
from .models import PurchaseRequestData, QuotationContentsData, PurchaseQuotationData
from .serializers import PurchaseRequestDataSerializer, QuotationContentsDataSerializer, PurchaseQuotationDataSerializer

# ViewSet for PurchaseRequestData
class PurchaseRequestView(viewsets.ModelViewSet):
    queryset = PurchaseRequestData.objects.all()
    serializer_class = PurchaseRequestDataSerializer

# ViewSet for QuotationContentsData
class QuotationContentsView(viewsets.ModelViewSet):
    queryset = QuotationContentsData.objects.all()
    serializer_class = QuotationContentsDataSerializer

# ViewSet for PurchaseQuotationData
class PurchaseQuotationView(viewsets.ModelViewSet):
    queryset = PurchaseQuotationData.objects.all()
    serializer_class = PurchaseQuotationDataSerializer
