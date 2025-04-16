from django.db import models
from feature_goods_tracking.models import VendorData
from feature_get_reference_data.models import *

class PurchaseRequestData(models.Model):
    request_id = models.CharField(max_length=255, primary_key=True)
    employee_id = models.ForeignKey(
        EmployeeData,
        db_column="employee_id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    class Meta:
        managed = False
        db_table = '"purchasing"."purchase_requests"'
        ordering = ["request_id"]

    def __str__(self):
        return str(self.request_id)


class QuotationContentsData(models.Model):
    quotation_content_id = models.CharField(max_length=255, primary_key=True)
    
    request_id = models.ForeignKey(
        PurchaseRequestData,
        db_column="request_id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    material_id = models.CharField(max_length=255)
    asset_id = models.CharField(max_length=255)
    purchase_quantity = models.PositiveIntegerField()
    
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = '"purchasing"."quotation_contents"'
        ordering = ["quotation_content_id"]

    def __str__(self):
        return str(self.quotation_content_id)


class PurchaseQuotationData(models.Model):
    quotation_id = models.CharField(max_length=255, primary_key=True)

    request_id = models.ForeignKey(
        PurchaseRequestData,
        db_column="request_id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    vendor_code = models.ForeignKey(
        VendorData,
        db_column="vendor_code",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    delivery_loc = models.CharField(max_length=255)
    freight = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = '"purchasing"."purchase_quotation"'
        ordering = ["quotation_id"]

    def __str__(self):
        return str(self.quotation_id)


class PurchaseOrderData(models.Model):  # <- corrected from models.model to models.Model
    purchase_id = models.CharField(max_length=255, primary_key=True)
    delivery_date = models.DateField()
    quotation_id = models.OneToOneField(  # one-to-one relationship with quotation
        PurchaseQuotationData,
        db_column="quotation_id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    document_date = models.DateField()

    class Meta:
        managed = False
        db_table = '"purchasing"."purchase_order"'
        ordering = ["purchase_id"]

    def __str__(self):
        return self.purchase_id
