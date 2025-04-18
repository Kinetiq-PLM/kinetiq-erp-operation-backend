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


class ProductCostDataView(viewsets.ReadOnlyModelViewSet):
    """View to retrieve Vendor Data"""
    queryset = ProductCostData.objects.all()
    serializer_class = ProductCostSerializer
    
    
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
                SELECT MAX(ar_credit_memo) 
                FROM operations.document_header 
                WHERE ar_credit_memo LIKE 'AR-%'
            """)
            last_credit_memo = cursor.fetchone()[0] or "AR-1000"  # Default starting point

            # Calculate next credit memo ID
            if last_credit_memo:
                last_number = int(last_credit_memo.split('-')[1])
                next_credit_memo = f"AR-{last_number + 1}"
            else:
                next_credit_memo = "AR-1000"

            return Response({
                "next_transaction_id": str(last_transaction_id + 1),
                "next_document_no": str(last_document_no + 1),
                "last_credit_memo_id": last_credit_memo,
                "next_credit_memo_id": next_credit_memo
            })

            return Response({
                "next_transaction_id": str(last_transaction_id + 1),
                "next_document_no": str(last_document_no + 1),
                "last_credit_memo_id": last_credit_memo,
                "next_credit_memo_id": next_credit_memo
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
                    (productdocu_id, asset_id, material_id, quantity, unit_cost, warehouse)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING content_id
                """, [
                    productdocu_id,
                    item.get('asset_id'),
                    item.get('material_id'),
                    item.get('quantity'),
                    item.get('unit_cost'),
                    item.get('warehouse'),

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
            
    @action(detail=False, methods=['post', 'get'], url_path='custom-create')
    def create_tracking(self, request):
        data = request.data
        document_items = data.get('document_items', [])

        try:
            cursor = connection.cursor()
            inserted_productdocu_ids = {}
            # 1. Insert into product_document_items
            for item in document_items:
                product_id = item.get('product_id')
                manuf_date = item.get('manuf_date')
                expiry_date = item.get('expiry_date')

                if not manuf_date:
                    manuf_date = date.today()
                if not expiry_date:
                    expiry_date = date.today() + timedelta(days=365)
                if product_id:
                    cursor.execute("""
                        INSERT INTO operations.product_document_items (product_id, manuf_date, expiry_date)
                        VALUES (%s, %s, %s)
                        RETURNING productdocu_id
                    """, [
                        product_id,
                        manuf_date,
                        expiry_date
                    ])
                    productdocu_id = cursor.fetchone()[0]
                    inserted_productdocu_ids[item.get('temp_id')] = productdocu_id

            # 2. Insert into document_items
            inserted_doc_item_ids = []
            for item in document_items:
                productdocu_id = inserted_productdocu_ids.get(item.get('temp_id')) or item.get('productdocu_id')
                cursor.execute("""
                    INSERT INTO operations.document_items 
                    (productdocu_id, asset_id, material_id, quantity, cost, warehouse_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING content_id
                """, [
                    productdocu_id,
                    item.get('asset_id'),
                    item.get('material_id'),
                    item.get('quantity'),
                    item.get('unit_cost'),
                    item.get('warehouse'),
                ])
                inserted_doc_item_ids.append(cursor.fetchone()[0])
            # 3. Insert into document_header
            
            cursor.execute("""
                INSERT INTO operations.document_header (
                    document_type, transaction_id, document_no, status, posting_date,
                    transaction_cost, vendor_code, buyer, employee_id,
                    delivery_date, document_date, initial_amount, discount_rate,
                    discount_amount, freight, tax_rate, tax_amount, ar_credit_memo, invoice_id
                ) VALUES (%s, %s, %s, %s, %s,
                          %s, %s, %s, %s,
                          %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s)
                RETURNING document_id
            """, [
                data.get('document_type'),
                data.get('transaction_id'),
                data.get('document_no'),
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
                data.get('tax_amount'),
                data.get('ar_credit_memo'),
                data.get('invoice_id')
            ])
            document_id = cursor.fetchone()[0]
            for content_id in inserted_doc_item_ids:
                cursor.execute("""
                    UPDATE operations.document_items
                    SET document_id = %s
                    WHERE content_id = %s
                """, [document_id, content_id])
            return Response({
                "message": "Created successfully",
                "document_id": document_id,
                "document_items": inserted_doc_item_ids,
                "product_docu_items": list(inserted_productdocu_ids.values())
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class createDocumentItem(viewsets.ViewSet):
    queryset = DocumentItems.objects.none()  # Dummy queryset
    serializer_class = DocumentItemsSerializer
    @action(detail=False, methods=['post'], url_path='create-product-docu-item')
    def create_product_docu_item(self, request):
        try:
            data = request.data
            product_id = data.get('product_id')
            if not product_id:
                return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            manuf_date = data.get('manuf_date') or datetime.date.today()
            expiry_date = data.get('expiry_date') or (manuf_date + datetime.timedelta(days=365))
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO operations.product_document_items (product_id, manuf_date, expiry_date)
                    VALUES (%s, %s, %s)
                    RETURNING productdocu_id;
                """, [
                    product_id,
                    manuf_date,
                    expiry_date
                ])
                productdocu_id = cursor.fetchone()[0]
            # Use ORM to return full data
            product_docu_item = ProductDocuItemData.objects.get(productdocu_id=productdocu_id)
            serializer = ProductDocuItemSerializer(product_docu_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='create-document-item')
    
    def create_document_item(self, request):
        try:
            data = request.data
            document_id = data.get('document_id')
            
            if not document_id:
                return Response({'error': 'document_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            if 'asset_id' in data:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO operations.serial_tracking (document_id)
                        VALUES (NULL)
                        RETURNING serial_id;
                    """, [document_id])
                    serial_id = cursor.fetchone()[0]
                serial_instance = SerialTrackingData.objects.get(serial_id=serial_id)
            else:
                serial_instance = None
            
            # === BATCH NO GENERATION ===
            today_str = datetime.datetime.now().strftime("%Y%m%d")
            prefix = f"BN{today_str}"

            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT batch_no FROM operations.document_items
                    WHERE batch_no LIKE %s
                    ORDER BY batch_no DESC
                    LIMIT 1;
                """, [f"{prefix}-%"])
                last_batch = cursor.fetchone()

            if last_batch:
                last_number = int(last_batch[0].split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            if 'productdocu_id' in data:
                batch_no = f"{prefix}-{str(new_number).zfill(4)}"
            else:
                batch_no = None
            # ===========================
            
            item_data = {
                'document_id': GoodsTrackingData.objects.get(document_id=document_id),
                'quantity': data.get('quantity', 0),
                'cost': data.get('cost', 0),
                'total': Decimal(data.get('quantity', 0)) * Decimal(data.get('cost', 0)),
                'warehouse_id': data.get('warehouse_id', 'DEFAULT_WAREHOUSE'),
                'batch_no': batch_no,
                'serial_id': serial_instance
            }

            if 'material_id' in data:
                item_data['material_id'] = MaterialData.objects.get(material_id=data['material_id'])
            elif 'asset_id' in data:
                item_data['asset_id'] = AssetData.objects.get(asset_id=data['asset_id'])
            elif 'productdocu_id' in data:
                item_data['productdocu_id'] = ProductDocuItemData.objects.get(productdocu_id=data['productdocu_id'])
            else:
                return Response({'error': 'No valid item type specified'}, status=status.HTTP_400_BAD_REQUEST)

            document_item = DocumentItems.objects.create(**item_data)

            goods_tracking = item_data['document_id']
            goods_tracking.transaction_cost += item_data['total']
            goods_tracking.save()

            serializer = DocumentItemsSerializer(document_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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