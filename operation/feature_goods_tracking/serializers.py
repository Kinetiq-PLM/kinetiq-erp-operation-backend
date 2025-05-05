from rest_framework import serializers
from feature_get_reference_data.models import *
from feature_get_reference_data.serializers import *

from .models import *

class ItemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemData
        fields = "__all__"  



class SalesInvoiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoiceData
        fields = "__all__"


class DocumentItemsSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item_id.item_name', read_only=True)
    item_type = serializers.CharField(source='item_id.item_type', read_only=True)
    unit_of_measure = serializers.CharField(source='item_id.unit_of_measure', read_only=True)
    purchase_date = serializers.DateField(source='item_id.purchase_date', read_only=True)
    class Meta:
        model = DocumentItems
        fields = "__all__"
        extra_kwargs = {
            'content_id': {'read_only': True}
        }
           
class GoodsTrackingDataSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    contact_person = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()
    dept_name = serializers.SerializerMethodField()
    document_items = DocumentItemsSerializer(many=True) 
    invoice_amount = serializers.SerializerMethodField()
    invoice_date = serializers.SerializerMethodField()
    invoice_id = serializers.SerializerMethodField()
    document_items = serializers.SerializerMethodField()

    def get_document_items(self, obj):
        # Get all document items
        doc_items = obj.document_items.all()
        
        # Collect all unique item_ids
        item_ids = [item.item_id for item in doc_items if item.item_id]
        
        # Fetch all related ItemData in one query
        items_data = ItemData.objects.filter(item_id__in=item_ids)
        items_dict = {item.item_id: item for item in items_data}
        
        # Build the result
        result = []
        for doc_item in doc_items:
            item_data = items_dict.get(doc_item.item_id)
            if item_data:
                result.append({
                    "content_id": doc_item.content_id,
                    "item_id": doc_item.item_id,
                    "item_name": item_data.item_name,
                    "item_price": doc_item.item_price,
                    "item_type": item_data.item_type,
                    "unit_of_measure": item_data.unit_of_measure,
                    "purchase_date": item_data.purchase_date,
                    "quantity": doc_item.quantity,
                    "ar_discount": doc_item.ar_discount,
                    "manuf_date": doc_item.manuf_date,
                    "expiry_date": doc_item.expiry_date,
                    "warehouse_id": doc_item.warehouse_id,
                    "item_no": doc_item.item_no
                })
        
        return result
    class Meta:
        model = GoodsTrackingData
        fields = "__all__"  
    def get_invoice_id(self, obj):
        try:
            return obj.invoice_id.invoice_id
        except (SalesInvoiceData.DoesNotExist, AttributeError):
            return None

    def get_invoice_amount(self, obj):
        try:
            return obj.invoice_id.total_amount
        except (SalesInvoiceData.DoesNotExist, AttributeError):
            return None

    def get_invoice_date(self, obj):
        try:
            return obj.invoice_id.invoice_date
        except (SalesInvoiceData.DoesNotExist, AttributeError):
            return None
    def get_vendor_name(self, obj):
        # Ensure that vendor is not None before accessing vendor_name
        if obj.vendor_code:
            return obj.vendor_code.company_name
        return None
    def get_contact_person(self, obj):
        if obj.vendor_code:
            return obj.vendor_code.contact_person
        return None
    def get_employee_name(self, obj):
        try:
            if obj.owner:
                return f"{obj.owner.first_name} {obj.owner.last_name}"
            return None
        except EmployeeData.DoesNotExist:
            return None

    def get_dept_name(self, obj):
        try:
            if obj.owner and obj.owner.dept_id:
                return obj.owner.dept_id.dept_name
            return None
        except EmployeeData.DoesNotExist:
            return None
    