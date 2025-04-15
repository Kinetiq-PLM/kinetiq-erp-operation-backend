from rest_framework import serializers
from .models import (
    PurchaseOrderData,
    PurchaseQuotationData,
    PurchaseRequestData,
    QuotationContentsData
)
from feature_goods_tracking.models import VendorData


class PurchaseRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    class Meta:
        model = PurchaseRequestData
        fields = "__all__"
    def get_employee_name(self, obj):
        if obj.employee_id:  
            return f"{obj.employee_id.first_name} {obj.employee_id.last_name}"
        return None  

class VendorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorData
        fields = ['vendor_code', 'vendor_name']  # add other fields as needed


class QuotationContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationContentsData
        fields = "__all__"


class PurchaseQuotationSerializer(serializers.ModelSerializer):
    vendor_code = VendorDataSerializer()
    request_id = PurchaseRequestSerializer()
    vendor_name = serializers.SerializerMethodField()
    contact_person = serializers.SerializerMethodField()
    
    class Meta:
        model = PurchaseQuotationData
        fields = "__all__"  
    def get_vendor_name(self, obj):
        # Ensure that vendor is not None before accessing vendor_name
        if obj.vendor_code:
            return obj.vendor_code.vendor_name
        return None
    def get_contact_person(self, obj):
        if obj.vendor_code:
            return obj.vendor_code.contact_person
        return None
    

class PurchaseOrderSerializer(serializers.ModelSerializer):
    quotation_id = PurchaseQuotationSerializer()
    quotation_contents = serializers.SerializerMethodField()
    
    class Meta:
        model = PurchaseOrderData
        fields = "__all__"  

    def get_quotation_contents(self, obj):
        if obj.quotation_id and obj.quotation_id.request_id:
            contents = QuotationContentsData.objects.filter(
                request_id=obj.quotation_id.request_id
            )
            return QuotationContentsSerializer(contents, many=True).data
        return []
    

