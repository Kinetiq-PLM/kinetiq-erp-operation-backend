from django.shortcuts import render
from .models import *
from .serializers import *
from django.db import connection
from django.shortcuts import get_object_or_404

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
    

class ExternalModuleProductView(viewsets.ModelViewSet):
    queryset = ExternalModuleProductOrderData.objects.all()
    serializer_class = ExternalModuleProductOrderSerializer

    @action(detail=False, methods=['post', 'get'], url_path='sync-production')
    def sync_production(self, request):

        try:
            with connection.cursor() as cursor:

                # Get all existing production_order_detail_ids from external module table
                cursor.execute("""
                    SELECT production_order_detail_id FROM operations.external_module
                """)
                existing_ids = set(row[0] for row in cursor.fetchall())

                # Get all production_order_detail_ids from production orders
                cursor.execute("""
                    SELECT production_order_detail_id
                    FROM production.production_orders_details
                """)
                all_ids = set(row[0] for row in cursor.fetchall())

                # Determine which IDs are missing
                missing_ids = all_ids - existing_ids

                # Insert missing entries into external_module_product_order and document_items
                inserted_count = 0
                for pid in missing_ids:
                    # Insert into external_module_product_order and get generated external_id
                    cursor.execute("""
                        INSERT INTO operations.external_module(
                            production_order_detail_id,
                            rework_quantity,
                            reason_rework
                        )
                        VALUES (%s, %s, %s)
                        RETURNING external_id;
                    """, [pid, 0, ""])

                    generated_external_id = cursor.fetchone()[0]
                    inserted_count += 1

                    # Insert into document_items with the generated external_id
                    cursor.execute("""
                        INSERT INTO operations.document_items (
                            external_id
                        )
                        VALUES (%s);
                    """, [generated_external_id])

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
                SELECT 
                    em.production_order_detail_id,
                    prod.product_name,
                    em.external_id,
                    em.rework_quantity,
                    em.reason_rework,
                    po.actual_quantity,
                    po.rework_required,
                    po.rework_notes
                FROM operations.external_module em
                JOIN production.production_orders_details po
                ON em.production_order_detail_id = po.production_order_detail_id
                LEFT JOIN production.production_orders_header poh
                    ON poh.production_order_id = po.production_order_id
                LEFT JOIN mrp.bill_of_materials bom_prod
                    ON bom_prod.bom_id = poh.bom_id
                LEFT JOIN mrp.product_mats pm_prod
                    ON pm_prod.product_mats_id = bom_prod.product_mats_id
                LEFT JOIN admin.products prod
                    ON prod.product_id = pm_prod.product_id
            """)
            rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "production_order_detail_id": row[0],
                "product_name" : row[1],
                "external_module": {
                    "external_id": row[2],
                    "rework_quantity": row[3],
                    "reason_rework": row[4]
                },
                "production_order": {
                    "actual_quantity": row[5],
                    "rework_required": row[6],
                    "rework_notes": row[7]
                }
            })
        result = sorted(result, key=lambda x: x['external_module']['reason_rework'] != '---')
        return Response(result)


    @action(detail=False, methods=['post', 'get'], url_path='update-rework')
    def update_rework_from_frontend(self, request):
        try:
            data = request.data
            
            # Ensure data is a list
            if not isinstance(data, list):
                data = [data]  # Convert single object to list
            
            updated = 0
            errors = []

            with connection.cursor() as cursor:
                for entry in data:
                    try:
                        prod_id = entry.get("production_order_detail_id")
                        quantity = entry.get("rework_quantity")
                        reason = entry.get("reason_rework")

                        if not prod_id:
                            errors.append(f"Missing production_order_detail_id in entry: {entry}")
                            continue

                        cursor.execute("""
                            UPDATE operations.external_module
                            SET rework_quantity = %s,
                                reason_rework = %s
                            WHERE production_order_detail_id = %s
                            RETURNING production_order_detail_id
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
