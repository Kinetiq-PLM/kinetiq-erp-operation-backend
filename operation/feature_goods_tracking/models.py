from django.db import models
from feature_get_reference_data.models import *
import datetime
from decimal import Decimal
# Create your models here.

class ItemData(models.Model):
    quotation_content_id = models.CharField(max_length=255, primary_key=True)
    item_id = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measure = models.CharField(max_length=255)
    purchase_date = models.DateField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = '"operations"."v_item_list_view"'
        ordering = ["item_id"]
        
    def __str__(self):
        return self.item_id
    
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

def get_default_employee():
    try:
        return None
    except EmployeeData.DoesNotExist:
        # Return just the ID (string) instead of an EmployeeData object
        return None
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
    posting_date = models.DateField(default=datetime.date.today, editable=True)
    transaction_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_note = models.CharField(max_length=255)
    #Vendor Container
    vendor_code = models.ForeignKey(
        VendorData, 
        db_column="vendor_code",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    ) 
    buyer = models.CharField(max_length=255, null=True, blank=True)
    owner =models.ForeignKey(
        EmployeeData, 
        db_column="owner",
        to_field="employee_id",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        default=None
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
    
    purchase_id = models.CharField(max_length=255, null=True, blank=True)

    
    class Meta:
        managed = False
        db_table = '"operations"."document_header"'
        ordering = ["-transaction_id"]
    
    def __str__(self):
        return self.document_id
    
class DocumentItems(models.Model):
    content_id = models.CharField(max_length=255, primary_key=True) 
    document_id = models.ForeignKey(
        GoodsTrackingData, 
        db_column="document_id", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="document_items"
    ) #this is connected to Goods Tracking data with many to one relationship it is possible that goods tracking data have many document_items
    item_id = models.CharField(max_length=255, null=True, blank=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_no = models.CharField(max_length=255, unique=True, blank=False, null=True)
    ar_discount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    manuf_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    warehouse_id = models.CharField(max_length=255, null=True)
    class Meta:
        managed = False
        db_table = '"operations"."document_items"'
        ordering = ["content_id"]
        
    def __str__(self):
        return self.content_id
    def get_item_data(self):
        """Returns all ItemData records matching this item_id"""
        return ItemData.objects.filter(item_id=self.item_id)

