from django.db import models
import datetime

# Create your models here.
class AssetRemovalData(models.Model):
    status_choice = [("Approved", "Approved"), ("Pending", "Pending")]
    external_id = models.CharField(primary_key=True,max_length=255)
    deprecation_report_id = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    reported_date = models.DateTimeField()
    deprecation_status = models.TextField(choices=status_choice, default="Pending")
    
    class Meta:
        managed = False
        db_table = '"operations"."v_item_removal_view"'
        ordering = ["reported_date"]
    def __str__(self):
        return self.external_id
    
class sendToManagement(models.Model):
    approval_id = models.CharField(primary_key=True, editable=False)
    external_id = models.CharField()
    status = models.CharField(default="pending")
    
    class Meta:
        managed = False
        db_table = '"management"."management_approvals"'
    def __str__(self):
        return self.approval_id