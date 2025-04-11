from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from .models import *
from .serializers import *


class ProductCostDataView(viewsets.ReadOnlyModelViewSet):
    """View to retrieve Vendor Data"""
    queryset = ProductCostData.objects.all()
    serializer_class = ProductCostSerializer
    
"""class VendorDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VendorData.objects.all()
    serializer_class = VendorDataSerializer
class DepartmentDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DepartmentData.objects.all()
    serializer_class = DepartmentDataSerializer
class EmployeeDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmployeeData.objects.select_related("dept_id").filter(dept_id__dept_name="Operations")
    serializer_class = EmployeeDataSerializer"""
    
class MaterialView(viewsets.ReadOnlyModelViewSet):
    queryset = MaterialData.objects.all()
    serializer_class = MaterialSerializer
class AssetView(viewsets.ReadOnlyModelViewSet):
    queryset = AssetData.objects.all()
    serializer_class = AssetSerializer
class ProductView(viewsets.ReadOnlyModelViewSet):
    queryset = ProductData.objects.all()
    serializer_class = ProductSerializer
class ProductDocuItemView(viewsets.ReadOnlyModelViewSet):
    queryset = ProductDocuItemData.objects.all()
    serializer_class = ProductDocuItemSerializer  
    lookup_field = 'productdocu_id'
    def update(self, request, *args, **kwargs):
        """Handle the update of Product Document Items."""
        item_id = kwargs.get('pk')  # The pk of the product document item being updated
        instance = self.get_object()

        # Update the main product document item data
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response(serializer.data)
    
"""class SupplierView(APIView):
    def get(self, request):  # Using 'get' instead of 'list'
        vendor_data = VendorDataSerializer(VendorData.objects.all(), many=True)
        employee_data = EmployeeDataSerializer(
            EmployeeData.objects.filter(dept_id__dept_name="Operations"), many=True
        )
        return Response({
            "vendors": vendor_data.data,
            "employees": employee_data.data
        })"""
        
class GoodsTrackingDataViewSet(viewsets.ModelViewSet):
    queryset = GoodsTrackingData.objects.all()
    serializer_class = GoodsTrackingDataSerializer
    lookup_field = 'document_id'

    def update(self, request, *args, **kwargs):
        document_id = kwargs.get('document_id') or kwargs.get('pk')
        instance = self.get_object()

        # Update the main document data
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    

    
class DocumentItemsViewSet(viewsets.ModelViewSet):
    """View to handle CRUD operations for Document Items"""
    queryset = DocumentItems.objects.all()
    serializer_class = DocumentItemsSerializer
    lookup_field = "content_id"
    
    def update(self, request, *args, **kwargs):
        """Handle the update of Document Items."""
        content_id = kwargs.get('content_id') or kwargs.get('pk')  # The pk of the document item being updated
        try:
            instance = self.get_object()

            # Update the main document item data
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()


            return Response(serializer.data)
        
        except ValidationError as e:
            # If there are validation errors, return them as a response
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Catch all other exceptions and return an error response
            return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET'])
def get_next_document_info(request):
    last_doc = GoodsTrackingData.objects.order_by('-document_no').first()
    next_document_no = last_doc.document_no + 1 if last_doc else 1
    next_transaction_id = last_doc.transaction_id + 1 if last_doc else 1
    return Response({
        "next_document_no": next_document_no,
        "next_transaction_id": next_transaction_id
    })