from rest_framework import serializers
from .models import *

class InternalTransferDeliveryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalTransferDeliveryRequestData
        fields = '__all__'

class updateDRWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = updateDeliveryRequestData
        fields = '__all__'
        read_only_fields = ['external_id']

class sendToDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = sendToDistributionData
        fields = '__all__'
        read_only_fields = ['del_order_id']

class getWarehouseIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = getWarehouseIDData
        fields = '__all__'
        
class InternalTransferReworkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalTransferReworkOrderData
        fields = '__all__'