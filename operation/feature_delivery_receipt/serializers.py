from rest_framework import serializers
from .models import *

class DeliveryReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryReceiptData
        fields = '__all__'

class BillingReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingReceiptData
        fields = '__all__'
    
class DeliveryReworkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryReworkOrderData
        fields = '__all__' 