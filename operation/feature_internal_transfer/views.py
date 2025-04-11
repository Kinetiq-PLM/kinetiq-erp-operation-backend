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

class updateDeliveryRequestView(viewsets.ModelViewSet):
    queryset = updateDeliveryRequestData.objects.all()
    serializer_class = updateDRWarehouseSerializer
    
    def update(self, request, pk=None):
        try:
            queryset = updateDeliveryRequestData.objects.get(content_id=pk)
            data = request.data

            queryset.warehouse_id = data.get('warehouse_id', queryset.warehouse_id)
            queryset.delivery_request_id = data.get('delivery_id', queryset.delivery_request_id)
            queryset.save()

            return Response({"message": "Delivery approval updated successfully"}, status=status.HTTP_200_OK)
        except updateDeliveryRequestData.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class sendToDistributionView(viewsets.ModelViewSet):
    queryset = sendToDistributionData.objects.all()
    serializer_class = sendToDistributionSerializer
    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save() 
                return Response({"message": "Inserted successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getWarehouseIDView(viewsets.ModelViewSet):
    queryset = getWarehouseIDData.objects.all()
    serializer_class = getWarehouseIDSerializer
    
class InternalTransferReworkOrderView(viewsets.ModelViewSet):
    queryset = InternalTransferReworkOrderData.objects.all()
    serializer_class = InternalTransferReworkOrderSerializer