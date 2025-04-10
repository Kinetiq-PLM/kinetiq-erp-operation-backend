from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


# Create your views here.
class InternalTransferDeliveryRequestView(viewsets.ModelViewSet):
    queryset = InternalTransferDeliveryRequestData.objects.all()
    serializer_class = InternalTransferDeliveryRequestSerializer

class updateDRWarehouseView(viewsets.ModelViewSet):
    queryset = updateDRWarehouseData.objects.all()
    serializer_class = updateDRWarehouseSerializer
    
    def update(self, request, pk=None):
        try:
            queryset = updateDRWarehouseData.objects.get(external_id=pk)
            data = request.data

            queryset.warehouse_id = data.get('approval_status', queryset.approval_status)
            queryset.save()

            return Response({"message": "Delivery approval updated successfully"}, status=status.HTTP_200_OK)
        except updateDRWarehouseData.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class getWarehouseIDView(viewsets.ModelViewSet):
    queryset = getWarehouseIDData.objects.all()
    serializer_class = getWarehouseIDSerializer
    
class InternalTransferReworkOrderView(viewsets.ModelViewSet):
    queryset = InternalTransferReworkOrderData.objects.all()
    serializer_class = InternalTransferReworkOrderSerializer