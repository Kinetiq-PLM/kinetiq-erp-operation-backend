from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# Create your views here.
class updateDeliveryApprovalView(viewsets.ModelViewSet):
    queryset = updateDeliveryApprovalData.objects.all()
    serializer_class = updateDeliveryApprovalSerializer

    def update(self, request, pk=None):
        try:
            queryset = updateDeliveryApprovalData.objects.get(approval_request_id=pk)
            data = request.data

            queryset.approval_status = data.get('approval_status', queryset.approval_status)
            queryset.approval_date = data.get('approval_date', queryset.approval_date)
            queryset.approved_by = data.get('approved_by', queryset.approved_by)
            queryset.save()

            return Response({"message": "Delivery approval updated successfully"}, status=status.HTTP_200_OK)
        except updateDeliveryApprovalData.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class DeliveryApprovalView(viewsets.ModelViewSet):
    queryset = DeliveryApprovalData.objects.all()
    serializer_class = DeliveryApprovalSerializer
    
    def update_delivery_approval(request, id):
        queryset = DeliveryApprovalData.objects.get(id=id)
        if request.method == "POST":
            data = request.POST
            approval_status = data.get('approval_status')
            approval_date = data.get('approval_date')
            approved_by =data.get('approved_by')
            
            queryset.approval_status = approval_status
            queryset.approval_date = approval_date
            queryset.approved_by = approved_by
            return 