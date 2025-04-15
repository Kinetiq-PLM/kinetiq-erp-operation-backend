from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from .models import *

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
class SupplierView(APIView):
    def get(self, request): 
        vendor_data = VendorDataSerializer(VendorData.objects.all(), many=True)
        employee_data = EmployeeDataSerializer(
            EmployeeData.objects.filter(dept_id__dept_name="Operations"), many=True
        )
        return Response({
            "vendors": vendor_data.data,
            "employees": employee_data.data
        })
class ItemView(APIView):
    def get(self, request): 
        products_data = ProductDataSerializer(ProductData.objects.all(), many=True)
        material_data = MaterialDataSerializer(MaterialData.objects.all(), many=True)
        asset_data = AssetDataSerializer(AssetData.objects.all(), many=True)
        return Response({
            "products": products_data.data,
            "material": material_data.data,
            "asset": asset_data.data
        })
class CustomerView(viewsets.ReadOnlyModelViewSet):
    queryset = CustomerData.objects.all()
    
    serializer_class = CustomerDataSerializer