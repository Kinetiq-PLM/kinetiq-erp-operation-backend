from django.db import models
from django.db.models import Case, When, Value, IntegerField

# Create your models here.
#class DeliveryApprovalData(models.Model):
class DeliveryApprovalData(models.Model):
    approval_choice = [("Approved", "Approved"), ("Pending", "Pending"), ("Rejected", "Rejected")]
    external_id = models.CharField(max_length=255, primary_key=True, unique=True)
    approval_request_id = models.CharField(max_length=255)
    request_date = models.DateField()
    approval_status = models.CharField(choices=approval_choice)
    approval_date = models.DateField()
    approved_by = models.CharField(max_length=100)
    
    class Meta:
        managed = False
        db_table = '"operations"."v_delivery_approval_view"'
        ordering = [
            Case(
                When(approval_status="Pending", then=Value(1)),
                When(approval_status="Approved", then=Value(2)),
                When(approval_status="Rejected", then=Value(3)),
                output_field=IntegerField(),
            ),
            "request_date",
        ]
        
    def __str__(self):
        return self.approval_request_id
    
class updateDeliveryApprovalData(models.Model):
    approval_choice = [("Approved", "Approved"), ("Pending", "Pending"), ("Rejected", "Rejected")]
    approval_request_id = models.CharField(max_length=255, primary_key=True)
    request_date = models.DateField()
    approval_status = models.CharField(choices=approval_choice)
    approval_date = models.DateField()
    approved_by = models.CharField(max_length=100)
    
    class Meta:
        managed = False
        db_table = '"distribution"."logistics_approval_request"'
        ordering = ["approval_request_id"]
        
    def __str__(self):
        return self.approval_request_id