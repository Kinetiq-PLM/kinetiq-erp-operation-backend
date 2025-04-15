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
    
class ProductData(models.Model):
    product_id =models.CharField(max_length=255,primary_key=True)
    product_name = models.CharField(max_length=255)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measure = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = '"admin"."products"'
        ordering = ["product_name"]
    def __str__(self):
        return self.product_id
class MaterialData(models.Model):
    material_id = models.CharField(max_length=255, primary_key=True)
    material_name = models.CharField(max_length=255)
    unit_of_measure = models.CharField(max_length=255)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        managed = False
        db_table = '"admin"."raw_materials"'
        ordering = ["material_name"]
    def __str__(self):
        return self.material_id
    
class AssetData(models.Model):
    asset_id = models.CharField(max_length=255, primary_key=True)
    asset_name = models.CharField(max_length=255)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        managed = False
        db_table = '"admin"."assets"'
        ordering = ["asset_name"]
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