from django.db import models

import datetime

# Create your models here.
class InternalTransferDeliveryRequestData(models.Model):
    delivery_id = models.CharField(max_length=255, primary_key=True)
    delivery_type = models.CharField(max_length=255)
    module_name = models.CharField(max_length=255)
    warehouse_location = models.CharField(max_length=255)
    request_date = models.DateField(default=datetime.date.today)
    quantity = models.PositiveBigIntegerField(default=0)
    class Meta:
        managed = False
        db_table = '"operations"."v_internal_delivery_request_view"'
        ordering = ["request_date"]
    def __str__(self):
        return self.delivery_id


class updateDeliveryRequestData(models.Model):
    content_id = models.CharField(max_length=255, primary_key=True)
    external_id = models.CharField(max_length=255)
    delivery_request_id = models.CharField(max_length=255)
    warehouse_id = models.CharField(max_length=255)
    class Meta:
            managed = False
            db_table = '"operations"."document_items"'

class sendToDistributionData(models.Model):
    del_order_id = models.CharField(max_length=255, primary_key=True)
    content_id = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = '"distribution"."delivery_order"'
        
class getWarehouseIDData(models.Model):
    warehouse_id = models.CharField(max_length=255, primary_key=True)
    warehouse_location = models.CharField(max_length=255)
    class Meta:
            managed = False
            db_table = '"admin"."warehouse"'

#Rework Order
#order id, reason for rework, rework, quantity
class ProductionOrderData(models.Model):
    production_order_detail_id = models.CharField(max_length=255, primary_key=True, editable = False)
    actual_quantity = models.PositiveIntegerField()
    rework_required = models.BooleanField(default=False)
    rework_notes = models.CharField(max_length=255)
    class Meta:
        db_table = '"production"."production_orders_details"'
        managed = False
        ordering = ["actual_quantity"]

class ExternalModuleProductOrderData(models.Model):
    external_id = models.CharField(max_length=255, primary_key=True)
    production_order_detail_id = models.ForeignKey(
        ProductionOrderData, 
        db_column="production_order_detail_id", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    rework_quantity = models.PositiveIntegerField()
    reason_rework = models.CharField(max_length=255)
    class Meta:
        ordering = ['production_order_detail_id'] 
    

    