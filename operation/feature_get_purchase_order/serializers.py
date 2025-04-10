# serializers.py
from rest_framework import serializers
from .models import PurchaseRequestData, QuotationContentsData, PurchaseQuotationData

class PurchaseRequestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequestData
        fields = '__all__'  # Include all fields from the model

class QuotationContentsDataSerializer(serializers.ModelSerializer):
    request_id = PurchaseRequestDataSerializer()  # Nested serializer for PurchaseRequestData

    class Meta:
        model = QuotationContentsData
        fields = '__all__'  # Include all fields from the model

class PurchaseQuotationDataSerializer(serializers.ModelSerializer):
    quotation_content_id = QuotationContentsDataSerializer()  # Nested serializer for QuotationContentsData

    class Meta:
        model = PurchaseQuotationData
        fields = '__all__'  # Include all fields from the model
