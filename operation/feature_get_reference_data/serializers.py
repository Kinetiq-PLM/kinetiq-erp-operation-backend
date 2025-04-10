from rest_framework import serializers
from .models import *

class VendorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorData
        fields = "__all__"  
        
class DepartmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentData  
        fields = "__all__"  #
        
class EmployeeDataSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    class Meta:
        model = EmployeeData  
        fields = "__all__"  #
    def get_employee_name(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"