from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from datetime import datetime, date, timedelta
from django.db import connection
from .models import *
from .serializers import *

class SalesInvoiceView(viewsets.ReadOnlyModelViewSet):
    queryset = SalesInvoiceData.objects.all()
    serializer_class = SalesInvoiceDataSerializer
        
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
    
    @action(detail=False, methods=['get'], url_path='get-next-doc-ids')
    def get_next_document_ids(self, request):
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT MAX(CAST(transaction_id AS INTEGER)) FROM operations.document_header")
            last_transaction_id = cursor.fetchone()[0] or 0

            cursor.execute("SELECT MAX(CAST(document_no AS INTEGER)) FROM operations.document_header")
            last_document_no = cursor.fetchone()[0] or 0

            cursor.execute("""
                SELECT MAX(CAST(SUBSTRING(ar_credit_memo FROM '\d+$') AS INTEGER))
                FROM operations.document_header
                WHERE ar_credit_memo LIKE 'AR-%'
            """)
            last_credit_number = cursor.fetchone()[0] or 0

            next_credit_memo_id = f"AR-{last_credit_number + 1}"
    
            return Response({
                "next_transaction_id": str(last_transaction_id + 1),
                "next_document_no": str(last_document_no + 1),
                "next_credit_memo_id": next_credit_memo_id
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
    def create(self, request, *args, **kwargs):
        data = request.data
        document_items = data.get('document_items', [])

        try:
            cursor = connection.cursor()
            inserted_productdocu_ids = {}
            # 1. Get next available document_id and transaction_id
            next_document_no, next_transaction_id = get_next_ids()

            # Set the document_id and transaction_id in the request data
            data['document_no'] = next_document_no
            data['transaction_id'] = next_transaction_id

            # 2. Insert into product_document_items if product_id exists
            for item in document_items:
                product_id = item.get('product_id')
                if product_id:
                    cursor.execute("""
                        INSERT INTO operations.product_document_items (product_id, manuf_date, expiry_date)
                        VALUES (%s, %s, %s)
                        RETURNING productdocu_id
                    """, [
                        product_id,
                        item.get('manuf_date'),
                        item.get('expiry_date')
                    ])
                    productdocu_id = cursor.fetchone()[0]
                    inserted_productdocu_ids[item.get('temp_id')] = productdocu_id  # use temp_id as reference

            # 3. Insert into document_items
            inserted_doc_item_ids = []
            for item in document_items:
                productdocu_id = inserted_productdocu_ids.get(item.get('temp_id')) or item.get('productdocu_id')

                cursor.execute("""
                    INSERT INTO operations.document_items 
                    (productdocu_id, asset_id, material_id, quantity, unit_cost, warehouse_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING content_id
                """, [
                    productdocu_id,
                    item.get('asset_id'),
                    item.get('material_id'),
                    item.get('quantity'),
                    item.get('unit_cost'),
                    item.get('warehouse_id'),

                ])
                inserted_doc_item_ids.append(cursor.fetchone()[0])

            # 4. Insert into document_header (GoodsTrackingData)
            cursor.execute("""
                INSERT INTO operations.document_header (
                    document_type, transaction_id, document_no, status, posting_date,
                    transaction_cost, vendor_code, buyer, employee_id,
                    delivery_date, document_date, initial_amount, discount_rate,
                    discount_amount, freight, tax_rate, tax_amount
                ) VALUES (%s, %s, %s, %s, %s,
                          %s, %s, %s, %s,
                          %s, %s, %s, %s,
                          %s, %s, %s, %s)
                RETURNING document_id
            """, [
                data.get('document_type'),
                next_transaction_id,  # use the incremented transaction_id
                next_document_no,     # use the incremented document_no
                data.get('status', 'Draft'),
                data.get('posting_date'),
                data.get('transaction_cost'),
                data.get('vendor_code'),
                data.get('buyer'),
                data.get('employee_id'),
                data.get('delivery_date'),
                data.get('document_date'),
                data.get('initial_amount'),
                data.get('discount_rate'),
                data.get('discount_amount'),
                data.get('freight'),
                data.get('tax_rate'),
                data.get('tax_amount')
            ])
            document_id = cursor.fetchone()[0]
            return Response({
                "message": "Created successfully",
                "document_id": document_id,
                "document_items": inserted_doc_item_ids,
                "product_docu_items": list(inserted_productdocu_ids.values())
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    @action(detail=False, methods=['post'], url_path='custom-create')
    def create_tracking(self, request):
        data = request.data
        document_items = data.get('document_items', [])

        try:
            cursor = connection.cursor()
            inserted_productdocu_ids = {}

            #Create document_header
            cursor.execute("""
                INSERT INTO operations.document_header (
                    document_type, vendor_code, document_no, transaction_id,
                    invoice_id, purchase_id, ar_credit_memo, status,
                    posting_date, delivery_date, document_date, buyer,
                    owner, delivery_note, initial_amount, discount_rate,
                    discount_amount, freight, tax_rate, tax_amount, transaction_cost,
                ) VALUES (%s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s, %s)
                RETURNING document_id
            """, [
                data.get('document_type'),
                data.get('vendor_code'),
                data.get('document_no'),
                data.get('transaction_id'),
                
                data.get('invoice_id'),
                data.get('purchase_id'),
                data.get('ar_credit_memo'),
                data.get('status'),
                
                data.get('posting_date'),
                data.get('delivery_date'),
                data.get('document_date'),
                data.get('buyer'),
                
                data.get('owner'),
                data.get('delivery_note'),
                data.get('initial_amount'),
                data.get('discount_rate'),
                
                data.get('discount_amount'),
                data.get('freight'),
                data.get('tax_rate'),
                data.get('tax_amount'),
                data.get('transaction_cost'),    
            ])
            document_id = cursor.fetchone()[0]
            for item in document_items:
                productdocu_id = inserted_productdocu_ids.get(item.get('temp_id')) or item.get('productdocu_id')
                cursor.execute("""
                    INSERT INTO operations.document_items (
                        document_id, item_id, manuf_date, expiry_date,
                        purchased_date, item_price, quantity, ar_discount,
                        total, warehouse_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING content_id
                """, [
                    document_id,
                    item.get('item_id'),
                    item.get('manuf_date'),
                    item.get('expiry_date'),
                    
                    item.get('purchased_date'),
                    item.get('item_price'),
                    item.get('quantity'),
                    item.get('ar_discount'),
                    
                    item.get('total'),
                    item.get('warehouse_id'),
                ])
                
            return Response({
                "message": "Created successfully",
                "document_id": document_id,
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentItemsViewSet(viewsets.ModelViewSet):
    """View to handle CRUD operations for Document Items"""
    queryset = DocumentItems.objects.all()
    serializer_class = DocumentItemsSerializer
    lookup_field = "content_id"
    
    def create(self, request, *args, **kwargs):
        """Handle the creation of Document Items."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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


class createDocumentItem(viewsets.ViewSet):
    queryset = DocumentItems.objects.none()  # Dummy queryset
    serializer_class = DocumentItemsSerializer


@api_view(['GET'])
def get_next_document_info(request):
    last_doc = GoodsTrackingData.objects.order_by('-document_no').first()
    next_document_no = last_doc.document_no + 1 if last_doc else 1
    next_transaction_id = last_doc.transaction_id + 1 if last_doc else 1
    return Response({
        "next_document_no": next_document_no,
        "next_transaction_id": next_transaction_id
    })
    

@api_view(['GET'])
def get_item_options(request):
    try:
        products = ProductData.objects.all()
        materials = MaterialData.objects.all()
        assets = AssetData.objects.all()
        
        product_serializer = ProductDataSerializer(products, many=True)
        material_serializer = MaterialDataSerializer(materials, many=True)
        asset_serializer = AssetDataSerializer(assets, many=True)
        
        return Response({
            'products': product_serializer.data,
            'materials': material_serializer.data,
            'assets': asset_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)