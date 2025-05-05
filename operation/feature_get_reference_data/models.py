from django.db import models
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
    
class VendorData(models.Model):
    vendor_code = models.CharField(max_length=255, primary_key=True)
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = '"purchasing"."vendors"'
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

class CustomerData(models.Model):
    customer_id = models.CharField(max_length=255, primary_key=True)
    contact_person = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = '"sales"."customers"'
        ordering = ["customer_id"]
    def __str__(self):
        return self.customer_id