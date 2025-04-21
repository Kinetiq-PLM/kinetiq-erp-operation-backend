from django.db import models
from feature_get_reference_data.models import *
import datetime
from decimal import Decimal
# Create your models here.

class ProductCostData(models.Model):
    bom_id = models.CharField(max_length=255, primary_key=True)
    product_id = models.CharField(max_length=255)
    cost_of_production = models.DecimalField(max_digits=10, decimal_places=2)
    miscellaneous_costs = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        managed = False
        db_table = '"operations"."v_product_details_view"'
        ordering = ["bom_id"]
        
    def __str__(self):
        return self.bom_id
     

class DepartmentData(models.Model):
    dept_id = models.CharField(max_length=255, primary_key=True)
    dept_name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = '"human_resources"."departments"'
        ordering = ["dept_id"]
        
    def __str__(self):
        return self.dept_id
    
class EmployeeData(models.Model):
    employee_id = models.CharField(max_length=255,primary_key=True)
    dept_id = models.ForeignKey(DepartmentData, db_column="dept_id", on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = '"human_resources"."employees"'
        ordering = ["employee_id"]
        
    def __str__(self):
        return self.employee_id

class MaterialData(models.Model):
    material_id = models.CharField(max_length=255,primary_key=True)
    material_name = models.CharField(max_length=255)
    unit_of_measure = models.CharField(max_length=255)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        managed = False
        db_table = '"admin"."raw_materials"'
    def __str__(self):
        return self.material_id

class AssetData(models.Model):
    asset_id = models.CharField(max_length=255, primary_key=True)
    asset_name = models.CharField(max_length=255)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    class Meta:
        managed = False
        db_table = '"admin"."assets"'
    def __str__(self):
        return self.asset_id

class ProductData(models.Model):
    product_id = models.CharField(max_length=255, primary_key=True)
    product_name = models.CharField(max_length=255)
    unit_of_measure = models.CharField(max_length=255)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    class Meta:
        managed = False
        db_table = '"admin"."products"'
    def __str__(self):
        return self.product_id
    
class SerialTrackingData(models.Model):
    serial_id = models.CharField(primary_key=True, editable=False, max_length=255)
    serial_no = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = '"operations"."serial_tracking"'
        ordering = ["serial_no"]

class ProductDocuItemData(models.Model):
    productdocu_id = models.CharField(max_length=255, primary_key=True, unique=False)
    product_id = models.ForeignKey(
        ProductData, 
        db_column="product_id", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="document_products"
    ) 
    manuf_date = models.DateField(default=datetime.date.today, editable=False)
    expiry_date = models.DateField(default=datetime.date.today, editable=False)
    class Meta:
        managed = False
        db_table = '"operations"."product_document_items"'
    def __str__(self):
        return self.productdocu_id

def get_default_employee():
    try:
        return EmployeeData.objects.get(employee_id="E001")
    except EmployeeData.DoesNotExist:
        # Return just the ID (string) instead of an EmployeeData object
        return "E001"
class SalesInvoiceData(models.Model):
    invoice_id = models.CharField(max_length=255, primary_key=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = '"sales"."sales_invoices"'
    def __str__(self):
        return self.invoice_id
        
class GoodsTrackingData(models.Model):
    status_choice = [("Open", "Open"), ("Closed", "Closed"), ("Cancelled", "Cancelled"), ("Draft", "Draft")]
    document_id = models.CharField(max_length=255, primary_key=True)
    document_type = models.CharField(max_length=255, null=False)
    ar_credit_memo =models.CharField(max_length=255)
    invoice_id = models.ForeignKey(
        SalesInvoiceData, 
        db_column="invoice_id", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    #Main GT UI
    transaction_id = models.CharField(max_length=255, null=False)
    document_no = models.CharField(max_length=255, null=True)
    status = models.TextField(choices=status_choice, default="Draft")
    posting_date = models.DateField(default=datetime.date.today, editable=False)
    transaction_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #Vendor Container
    vendor_code = models.ForeignKey(
        VendorData, 
        db_column="vendor_code", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    ) #this is a foreign key how to make this so that i can get name and contact person
    buyer = models.CharField(max_length=255)
    employee_id =models.ForeignKey(
        EmployeeData, 
        db_column="employee_id", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        default=get_default_employee 
    ) #Owner
    #Document Details
    delivery_date = models.DateField(default=datetime.date.today)
    document_date = models.DateField(default=datetime.date.today)
    #Cost Details    
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    freight = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)

    
    class Meta:
        managed = False
        db_table = '"operations"."document_header"'
        ordering = ["-transaction_id"]
    
    def __str__(self):
        return self.document_id
    
class DocumentItems(models.Model):
    content_id = models.CharField(max_length=255, primary_key=True) 
    batch_no = models.CharField(max_length=255, auto_created=True, unique=True)

    document_id = models.ForeignKey(
        GoodsTrackingData, 
        db_column="document_id", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="document_items"
    ) #this is connected to Goods Tracking data with many to one relationship it is possible that goods tracking data have many document_items
    asset_id = models.ForeignKey(
        AssetData, 
        db_column="asset_id", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="document_assets"
    ) 
    material_id = models.ForeignKey(
        MaterialData, 
        db_column="material_id", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="document_materials"
    ) 
    productdocu_id = models.ForeignKey(
        ProductDocuItemData, 
        db_column="productdocu_id", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="document_product_items"
    ) 
    serial_id = models.OneToOneField(
        SerialTrackingData, 
        db_column="serial_id", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="document_serial_id"
    )
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    batch_no = models.CharField(max_length=255)
    warehouse_id = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        managed = False
        db_table = '"operations"."document_items"'
        ordering = ["content_id"]
        
    def __str__(self):
        return self.content_id
    

