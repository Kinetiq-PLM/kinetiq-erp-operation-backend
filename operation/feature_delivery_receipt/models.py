from django.db import models

# Create your models here.

class DeliveryReceiptData(models.Model):
    external_id = models.CharField(max_length=255, primary_key=True)
    delivery_receipt_id = models.CharField(max_length=255)
    delivery_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        managed = False
        db_table = '"operations"."v_delivery_receipt_view"'
        ordering = ["external_id"]
    def __str__(self):
        return self.external_id

class BillingReceiptData(models.Model):
    external_id = models.CharField(max_length=255, primary_key=True)
    billing_receipt_id = models.CharField(max_length=255)
    delivery_receipt_id = models.CharField(max_length=255)
    delivery_date = models.DateField()
    total_receipt = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        managed = False
        db_table = '"operations"."v_delivery_billing_receipt_view"'
        ordering = ["external_id"]
    def __str__(self):
        return self.external_id

class DeliveryReworkOrderData(models.Model):
    external_id = models.CharField(max_length=255, primary_key=True)
    rework_id = models.CharField(max_length=255,)
    failed_shipment_id = models.CharField(max_length=255)
    rework_status = models.CharField(max_length=255)
    rework_date = models.DateField()
    
    class Meta:
        managed = False
        db_table = '"operations"."v_delivery_rework_order_view"'
        ordering = ["external_id"]
        
    def __str__(self):
        return self.external_id