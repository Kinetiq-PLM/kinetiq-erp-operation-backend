from rest_framework import serializers
from feature_get_reference_data.models import *
from feature_get_reference_data.serializers import *

from .models import *

class ProductCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCostData
        fields = "__all__"  

"""class VendorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorData
        fields = "__all__"  
        
class DepartmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentData  
        fields = "__all__"  #
        
class EmployeeDataSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    class Meta:
        model = EmployeeData  
        fields = "__all__"  #
    def get_employee_name(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"""

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialData
        fields = "__all__"
        
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetData
        fields = "__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductData
        fields = "__all__"
        
class SerialTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerialTrackingData
        fields = "__all__"
class SalesInvoiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoiceData
        fields = "__all__"
class ProductDocuItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductDocuItemData
        fields = "__all__"
    def get_product_name(self, obj):
        # Safely access product_name and return "N/A" if product_id is None
        if obj.product_id:
            return obj.product_id.product_name
        return "N/A"  # Return "N/A" if product_id is None

class DocumentItemsSerializer(serializers.ModelSerializer):
    product_details = ProductDocuItemSerializer(source="productdocu_id", read_only=True)
    cost = serializers.SerializerMethodField() 
    unit_of_measure = serializers.SerializerMethodField()
    production_cost = serializers.SerializerMethodField()
    item_id = serializers.SerializerMethodField()
    item_name = serializers.SerializerMethodField()
    serial_no = serializers.SerializerMethodField()
    purchase_date = serializers.SerializerMethodField()
    class Meta:
        model = DocumentItems
        fields = "__all__"
        extra_kwargs = {
            'content_id': {'read_only': True}
        }
    def get_serial_no(self, obj):
        if obj.serial_id:
            return obj.serial_id.serial_no
    def get_purchase_date(self, obj):
        if obj.asset_id:
            return obj.asset_id.purchase_date
        return "N/A"
    def get_cost(self, obj):
        if obj.productdocu_id and obj.productdocu_id.product_id:
            return obj.productdocu_id.product_id.selling_price
        elif obj.material_id:
            return obj.material_id.cost_per_unit
        elif obj.asset_id:
            return obj.asset_id.purchase_price
        return "N/A"
    def get_unit_of_measure(self, obj,):
        if obj.productdocu_id and obj.productdocu_id.product_id:
            return obj.productdocu_id.product_id.unit_of_measure
        elif obj.material_id:
            return obj.material_id.unit_of_measure
        return "N/A"
    def get_item_id(self, obj):
        if obj.productdocu_id and obj.productdocu_id.product_id:
            return obj.productdocu_id.product_id.product_id
        elif obj.material_id:
            return obj.material_id.material_id
        elif obj.asset_id:
            return obj.asset_id.asset_id
        return "N/A"
    def get_item_name(self, obj):
        if obj.productdocu_id and obj.productdocu_id.product_id:
            return obj.productdocu_id.product_id.product_name
        elif obj.material_id:
            return obj.material_id.material_name
        elif obj.asset_id:
            return obj.asset_id.asset_name
        return "N/A"
    def get_production_cost(self, obj):
        if obj.productdocu_id and obj.productdocu_id.product_id:
            cost_data = ProductCostData.objects.filter(product_id=obj.productdocu_id.product_id.product_id).first()
            if cost_data:
                return cost_data.cost_of_production + cost_data.miscellaneous_costs if cost_data else Decimal("0.00")
        return Decimal("0.00")
    def create(self, validated_data):
        material_data = validated_data.get('material_id', None)
        asset_data = validated_data.get('asset_id', None)
        product_data = validated_data.get('productdocu_id', None)

        # Ensure only one of the three fields is provided
        if not any([material_data, asset_data, product_data]):
            raise serializers.ValidationError("At least one of material_id, asset_id, or productdocu_id must be provided.")

        return super().create(validated_data)
           
class GoodsTrackingDataSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    contact_person = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()
    dept_name = serializers.SerializerMethodField()
    document_items = DocumentItemsSerializer(many=True) 
    invoice_amount = serializers.SerializerMethodField()
    invoice_date = serializers.SerializerMethodField()
    
    class Meta:
        model = GoodsTrackingData
        fields = "__all__"  
    def get_invoice_amount(self, obj):
        if obj.invoice_id:
            return obj.invoice_id.total_amount
    def get_invoice_date(self, obj):
        if obj.invoice_id:
            return obj.invoice_id.invoice_date
    def get_vendor_name(self, obj):
        # Ensure that vendor is not None before accessing vendor_name
        if obj.vendor_code:
            return obj.vendor_code.vendor_name
        return None
    def get_contact_person(self, obj):
        if obj.vendor_code:
            return obj.vendor_code.contact_person
        return None
    def get_employee_name(self, obj):
        if obj.employee_id:  
            return f"{obj.employee_id.first_name} {obj.employee_id.last_name}"
        return None  

    def get_dept_name(self, obj):
        if obj.employee_id and obj.employee_id.dept_id:  
            return obj.employee_id.dept_id.dept_name  
        return None  

    