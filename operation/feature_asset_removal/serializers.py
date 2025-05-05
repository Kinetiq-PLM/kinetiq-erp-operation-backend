from rest_framework import serializers
from .models import *

class AssetRemovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetRemovalData
        fields = '__all__'

class sendToManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = sendToManagement
        fields = '__all__'
        read_only_fields = ['approval_id'] 