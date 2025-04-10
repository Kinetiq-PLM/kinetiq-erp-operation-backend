from django.db import models

# Create your models here.
class InternalTransferDeliveryRequestData(models.Model):
    external_id = models.CharField(max_length=255, primary_key=True)
    delivery_id = models.CharField(max_length=255)
    delivery_type = models.CharField(max_length=255)
    warehouse_id = models.CharField(max_length=255)
    module_name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = '"operations"."v_internal_delivery_request_view"'
    def __str__(self):
        return self.external_id
    
class updateDRWarehouseData(models.Model):
    content_id = models.CharField(max_length=255, primary_key=True)
    external_id = models.CharField(max_length=255)
    warehouse_id = models.CharField(max_length=255)
    class Meta:
            managed = False
            db_table = '"operations"."document_items"'
            
class getWarehouseIDData(models.Model):
    warehouse_id = models.CharField(max_length=255, primary_key=True)
    class Meta:
            managed = False
            db_table = '"admin"."warehouse"'
            
class InternalTransferReworkOrderData(models.Model):
    external_id = models.CharField(max_length=255, primary_key=True)
    product_id = models.CharField(max_length=255)
    start_date = models.DateField()
    rework_notes = models.CharField(max_length=255)
    selling_price = models.DecimalField(decimal_places=4,max_digits=10)