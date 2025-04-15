from rest_framework import viewsets
from .models import *
from .serializers import *
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class DeliveryReceiptView(viewsets.ModelViewSet):
    queryset = DeliveryReceiptData.objects.all()
    serializer_class = DeliveryReceiptSerializer
    
    @action(detail=False, methods=['post', 'get'], url_path='sync-deliveryreceipt')
    def sync_production(self, request):

        try:
            with connection.cursor() as cursor:


                # Get all existing delivery_receipt_id from external module table
                cursor.execute("""
                    SELECT delivery_receipt_id
                    FROM operations.external_module
                    WHERE delivery_receipt_id IS NOT NULL
                """)
                existing_ids = set(row[0] for row in cursor.fetchall())


                # Get all production_order_detail_ids from distribution delivery_receipt
                cursor.execute("""
                    SELECT delivery_receipt_id
                    FROM distribution.delivery_receipt
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
                            delivery_receipt_id
                        )
                        VALUES (%s)
                        RETURNING external_id;
                    """, [pid])

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

class BillingReceiptView(viewsets.ModelViewSet):
    queryset = BillingReceiptData.objects.all()
    serializer_class = BillingReceiptSerializer
    
    @action(detail=False, methods=['post', 'get'], url_path='sync-billingreceipt')
    def sync_production(self, request):
        try:
            with connection.cursor() as cursor:
                # Get all existing billing_receipt_id from external module table
                cursor.execute("""
                    SELECT billing_receipt_id
                    FROM operations.external_module
                    WHERE delivery_receipt_id IS NOT NULL
                """)
                existing_ids = set(row[0] for row in cursor.fetchall())


                # Get all billing_receipt_id from distribution billing_receipt
                cursor.execute("""
                    SELECT billing_receipt_id
                    FROM distribution.billing_receipt
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
                            billing_receipt_id
                        )
                        VALUES (%s)
                        RETURNING external_id;
                    """, [pid])

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

class DeliveryReworkOrderView(viewsets.ModelViewSet):
    queryset = DeliveryReworkOrderData.objects.all()
    serializer_class = DeliveryReworkOrderSerializer
    @action(detail=False, methods=['post', 'get'], url_path='sync-deliveryreworkorder')
    def sync_production(self, request):
        try:
            with connection.cursor() as cursor:
                # Get all existing rework_id from external module table
                cursor.execute("""
                    SELECT rework_id
                    FROM operations.external_module
                    WHERE delivery_receipt_id IS NOT NULL
                """)
                existing_ids = set(row[0] for row in cursor.fetchall())


                # Get all rework_id from distribution rework_order
                cursor.execute("""
                    SELECT rework_id
                    FROM distribution.rework_order
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
                            rework_id
                        )
                        VALUES (%s)
                        RETURNING external_id;
                    """, [pid])

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

class ExternalGoodsIssueView(viewsets.ModelViewSet):
    queryset = ExternalGoodsIssueData.objects.all()
    serializer_class = ExternalGoodsIssueSerializer
    @action(detail=False, methods=['post', 'get'], url_path='sync-deliverygoodsissue')
    def sync_production(self, request):
        try:
            with connection.cursor() as cursor:
                # Get all existing goods_issue_id from external module table
                cursor.execute("""
                    SELECT goods_issue_id
                    FROM operations.external_module
                    WHERE delivery_receipt_id IS NOT NULL
                """)
                existing_ids = set(row[0] for row in cursor.fetchall())


                # Get all rework_id from distribution rework_order
                cursor.execute("""
                    SELECT goods_issue_id
                    FROM distribution.goods_issue
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
                            goods_issue_id
                        )
                        VALUES (%s)
                        RETURNING external_id;
                    """, [pid])

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