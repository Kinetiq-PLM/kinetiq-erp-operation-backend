from rest_framework import serializers
from .models import *

class updateDeliveryApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = updateDeliveryApprovalData
        fields = "__all__"
        read_only_fields = ["approval_request_id"]
class DeliveryApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryApprovalData
        fields = '__all__'
