from django.shortcuts import render
from rest_framework import viewsets
from serializers import *
from models import *

# Create your views here.
class VendorDataViewSet(viewsets.ReadOnlyModelViewSet):
    """View to retrieve Vendor Data"""
    queryset = VendorData.objects.all()
    serializer_class = VendorDataSerializer
class DepartmentDataViewSet(viewsets.ReadOnlyModelViewSet):
    """View to retrieve Vendor Data"""
    queryset = DepartmentData.objects.all()
    serializer_class = DepartmentDataSerializer
class EmployeeDataViewSet(viewsets.ReadOnlyModelViewSet):
    """View to retrieve Vendor Data"""
    queryset = EmployeeData.objects.select_related("dept_id").filter(dept_id__dept_name="Operations")
    serializer_class = EmployeeDataSerializer