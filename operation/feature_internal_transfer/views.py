from django.shortcuts import render
from .models import *
from .serializers import *
from django.db import connection
from django.shortcuts import get_object_or_404
import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Q


# Create your views here.
class InternalTransferDeliveryRequestView(viewsets.ModelViewSet):
    queryset = InternalTransferDeliveryRequestData.objects.all()
    serializer_class = InternalTransferDeliveryRequestSerializer

class updateDeliveryRequestView(viewsets.ModelViewSet):
    queryset = updateDeliveryRequestData.objects.filter(
        Q(external_id__startswith='PROD-POD') | Q(external_id__startswith='PROJ-EPRM')
    )
    serializer_class = updateDRWarehouseSerializer
    def update(self, request, pk=None):
        try:
            data = request.data
            warehouse_id = data.get('warehouse_id')
            delivery_id = data.get('delivery_id') 

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 1 FROM operations.document_items
                    WHERE external_id = %s
                """, [delivery_id])
                if cursor.fetchone() is None:
                    return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

                cursor.execute("""
                    UPDATE operations.document_items
                    SET warehouse_id = %s
                    WHERE external_id = %s
                """, [warehouse_id, delivery_id])

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
    queryset = getWarehouseIDData.objects.exclude(warehouse_location__startswith='ARCHIVED')
    serializer_class = getWarehouseIDSerializer
    

class ExternalModuleProductView(viewsets.ModelViewSet):
    queryset = ExternalModuleProductOrderData.objects.all()
    serializer_class = ExternalModuleProductOrderSerializer
    
    @action(detail=False, methods=['post', 'get'], url_path='sync-production')
    def sync_production(self, request):

        try:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT external_id
                    FROM operations.document_items
                    WHERE document_items.external_id LIKE 'PROD-POD%';
                """)
                existing_ids = set(row[0] for row in cursor.fetchall())

                cursor.execute("""
                    SELECT production_order_detail_id
                    FROM production.production_orders_details
                """)
                all_ids = set(row[0] for row in cursor.fetchall())

                missing_ids = all_ids - existing_ids

                inserted_count = 0
                today = datetime.date.today()
                for pid in missing_ids:
                    cursor.execute("""
                        INSERT INTO operations.document_items(
                            external_id,
                            quantity,
                            reason_rework,
                            request_date
                        )
                        VALUES (%s, %s, %s, %s)
                        RETURNING content_id;
                    """, [pid, 0, "", today])

                    generated_external_id = cursor.fetchone()[0]
                    inserted_count += 1
                    

                return Response({
                    'status': 'success',
                    'message': f'{inserted_count} new records inserted into external_module_product_order and document_items.'
                })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=500)


    @action(detail=False, methods=['get'], url_path='rework-order')
    def fetch_all_joined(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM operations.v_internal_rework_details
            """)
            rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "rework_id": row[0],
                "product_name" : row[1],
                "reason_rework" : row[2],
                "actual_quantity" : row[3],
                "quantity" : row[4]
            })
        result = sorted(result, key=lambda x: (x['reason_rework'] or '').strip() != '')

        return Response(result)


    @action(detail=False, methods=['post', 'get'], url_path='update-rework')
    def update_rework_from_frontend(self, request):
        try:
            data = request.data
            
            if not isinstance(data, list):
                data = [data]  
            
            updated = 0
            errors = []

            with connection.cursor() as cursor:
                for entry in data:
                    try:
                        prod_id = entry.get("production_order_detail_id")
                        quantity = entry.get("quantity")
                        reason = entry.get("reason_rework")

                        if not prod_id:
                            errors.append(f"Missing production_order_detail_id in entry: {entry}")
                            continue

                        cursor.execute("""
                            UPDATE operations.document_items
                            SET quantity = %s,
                                reason_rework = %s
                            WHERE external_id = %s
                            RETURNING external_id
                        """, (quantity, reason, prod_id))

                        if cursor.rowcount == 0:
                            errors.append(f"No record found for production_order_detail_id: {prod_id}")
                        else:
                            updated += cursor.rowcount

                    except Exception as e:
                        errors.append(f"Error updating record {prod_id}: {str(e)}")

            if errors:
                return Response({
                    'status': 'partial_success',
                    'updated_rows': updated,
                    'errors': errors
                }, status=status.HTTP_207_MULTI_STATUS)

            return Response({
                'status': 'success',
                'updated_rows': updated
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
