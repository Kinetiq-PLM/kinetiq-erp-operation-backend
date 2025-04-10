from django.db import models

class VendorData(models.Model):
    vendor_code = models.CharField(max_length=255, primary_key=True)
    vendor_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = '"admin"."vendor"'
        ordering = ["vendor_code"]
        
    def __str__(self):
        return self.vendor_code

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
