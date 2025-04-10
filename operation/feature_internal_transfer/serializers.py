from rest_framework import serializers
from .models import *

class InternalTransferDeliveryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalTransferDeliveryRequestData
        fields = '__all__'

class updateDRWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = updateDRWarehouseData
        fields = '__all__'
        
class getWarehouseIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = getWarehouseIDData
        fields = '__all__'
        
class InternalTransferReworkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalTransferReworkOrderData
        fields = '__all__'