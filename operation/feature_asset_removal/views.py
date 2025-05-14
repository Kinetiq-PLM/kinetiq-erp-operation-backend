from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class AssetRemovalView(viewsets.ModelViewSet):
    queryset = AssetRemovalData.objects.all()
    serializer_class = AssetRemovalSerializer
    
class sendToManagementView(viewsets.ModelViewSet):
    queryset = sendToManagement.objects.all()
    serializer_class = sendToManagementSerializer
    

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)  
            if serializer.is_valid():
                serializer.save()  
                return Response(
                    {"message": "Inserted successfully", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {"error": "Invalid data", "details": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)