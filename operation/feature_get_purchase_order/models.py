from django.db import models
from feature_goods_tracking.models import VendorData
# Create your models here.

class PurchaseRequestData(models.Model):
    request_id = models.CharField(max_length=255, primary_key=True)
    material_id = models.CharField(max_length=255)
    asset_id = models.CharField(max_length=255)
    purchase_quantity = models.PositiveIntegerField()

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
        blank=True,
    )
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
    STATUS_CHOICES = [("Approved", "Approved"), ("Pending", "Pending"), ("Rejected", "Rejected")]

    quotation_id = models.CharField(max_length=255, primary_key=True)
    vendor_code = models.ForeignKey(
        VendorData, db_column="vendor_code", on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.TextField(choices=STATUS_CHOICES, default="Pending")
    document_no = models.PositiveIntegerField()
    document_date = models.TextField()
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2)
    freight = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)

    quotation_content_id = models.ForeignKey(
        QuotationContentsData,
        db_column="quotation_content_id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        managed = False
        db_table = '"purchasing"."purchase_quotation"'
        ordering = ["quotation_id"]

    def __str__(self):
        return str(self.quotation_id)

    